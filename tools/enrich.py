#!/usr/bin/env python3
"""Fill the owner (asn, isp, org, country) of networks that have none and regroup the blocks.

Networks without an owner come from tools/import_sources.py --no-lookup or are added by hand as a block with only
an `ip:` list. Owners come from the ip-api.com batch API and are cached in ~/.cache/scannersdb/ipapi.json.

usage: python3 tools/enrich.py [--refresh] [ID ...]

  ID          only these records (default: all)
  --refresh   ask again for every network of the records, also those that have an owner; hand corrections of
              isp / org are replaced
"""
import argparse
import ipaddress
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scdb  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    ids = args.ids or scdb.ids()
    records = [scdb.load(rid) for rid in ids]

    wanted = set()
    for rec in records:
        for fam in (4, 6):
            known = {} if args.refresh else scdb.block_info(rec, fam)
            for n in scdb.remove_subsumed(scdb.nets(rec, fam)):
                if not known.get(scdb.fmt(n)):
                    wanted.add(str(n.network_address))
    if wanted:
        print("looking up %d networks at ip-api.com" % len(wanted), file=sys.stderr)
        scdb.lookup(sorted(wanted, key=lambda a: ipaddress.ip_address(a).packed), refresh=args.refresh)

    changed = 0
    for rid in ids:
        rec = scdb.load(rid)    # read again: the lookups can take long and the file may have been edited meanwhile
        before = scdb.dump(rec)
        for fam in (4, 6):
            if rec.get("ipv%d" % fam):
                scdb.rebuild(rec, fam, fresh=args.refresh)
        if scdb.dump(rec) != before:
            rec["updated"] = scdb.today()
            scdb.save(rec)
            changed += 1
    print("records changed: %d of %d" % (changed, len(records)))


if __name__ == "__main__":
    main()

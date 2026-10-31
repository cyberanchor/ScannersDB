#!/usr/bin/env python3
"""Find which records hold an address or network, for example an address from a firewall log.

usage: python3 tools/where.py ADDRESS [ADDRESS ...]
       grep -oE '([0-9]{1,3}\\.){3}[0-9]{1,3}' /var/log/messages | sort -u | python3 tools/where.py -

Prints the record, its legal entity, the network that matches and its owner. When ~/.cache/scannersdb/provenance.json
exists (written by tools/import_sources.py), it also prints which upstream lists have that network.
"""
import bisect
import ipaddress
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scdb  # noqa: E402


def index(records):
    """Per family: rows (start, end, network, record, block) sorted by start, their starts, and the running maximum
    of their ends, so a search can stop as soon as no earlier network can reach the query."""
    out = {}
    for fam in (4, 6):
        rows = []
        for rec in records:
            for block in rec.get("ipv%d" % fam) or []:
                for text in block["ip"]:
                    n = ipaddress.ip_network(text)
                    rows.append((int(n.network_address), int(n.broadcast_address), text, rec, block))
        rows.sort(key=lambda x: (x[0], x[1]))
        top, reach = -1, []
        for r in rows:
            top = max(top, r[1])
            reach.append(top)
        out[fam] = (rows, [r[0] for r in rows], reach)
    return out


def find(idx, query):
    q = ipaddress.ip_network(query, strict=False)
    rows, starts, reach = idx[q.version]
    lo, hi = int(q.network_address), int(q.broadcast_address)
    hits = []
    i = bisect.bisect_right(starts, lo) - 1
    while i >= 0 and reach[i] >= hi:
        if rows[i][1] >= hi:
            hits.append(rows[i][2:])
        i -= 1
    return hits


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args == ["-"]:
        args = [line.strip() for line in sys.stdin if line.strip()]
    records = scdb.load_all()
    idx = index(records)
    try:
        with open(os.path.join(scdb.CACHE, "provenance.json"), encoding="utf-8") as f:
            prov = json.load(f)
    except (OSError, ValueError):
        prov = {}
    found = 0
    for a in args:
        try:
            hits = find(idx, a)
        except ValueError:
            print("%s: not an address" % a)
            continue
        if not hits:
            print("%s: not in ScannersDB" % a)
            continue
        found += 1
        for text, rec, block in hits:
            owner = ", ".join(x for x in (block.get("asn"), block.get("isp"), block.get("org"), block.get("country"))
                              if x)
            print("%s: %s (%s%s) in %s [%s]" % (a, rec["name"], rec["id"], ", " + rec["legal_entity"]
                                               if rec.get("legal_entity") else "", text, owner))
            up = prov.get(rec["id"], {})
            srcs = sorted({s for net, ss in up.items() for s in ss
                           if ipaddress.ip_network(net).version == ipaddress.ip_network(text).version
                           and ipaddress.ip_network(text).overlaps(ipaddress.ip_network(net))})
            if srcs:
                print("    listed by: %s" % ", ".join(srcs))
    sys.exit(0 if found else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Write hand-checked fields into records, from a YAML file:

    censys:
      legal_entity: Censys, Inc.
      flag: 🇺🇸
      country: United States
      note: null          # null removes the field

Lists replace the old value. Networks (ipv4, ipv6) are not set here: tools/import_sources.py adds them and
tools/enrich.py fills their owners. Records must exist; a key `rename: <new id>` renames the file.

usage: python3 tools/set_fields.py CHANGES.yaml [--dry-run]
"""
import argparse
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scdb  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("changes")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with open(args.changes, encoding="utf-8") as f:
        changes = yaml.safe_load(f) or {}
    existing = set(scdb.ids())
    errors = []
    for rid, fields in changes.items():
        if rid not in existing:
            errors.append("%s: no such record" % rid)
            continue
        for k in fields or {}:
            if k in ("ipv4", "ipv6", "id"):
                errors.append("%s: %s cannot be set here" % (rid, k))
            elif k not in scdb.KEYS and k != "rename":
                errors.append("%s: unknown field %r" % (rid, k))
    if errors:
        sys.exit("\n".join(errors))
    changed = 0
    for rid, fields in changes.items():
        rec = scdb.load(rid)
        before = scdb.dump(rec)
        new_id = (fields or {}).get("rename")
        for k, v in (fields or {}).items():
            if k == "rename":
                continue
            if v is None:
                rec.pop(k, None)
            else:
                rec[k] = v
        problems = scdb.check(rec)
        if problems:
            print("%s: %s" % (rid, "; ".join(problems)), file=sys.stderr)
        if new_id and new_id != rid:
            if new_id in existing:
                sys.exit("%s: cannot rename to %s, the record exists" % (rid, new_id))
            if not args.dry_run:
                os.remove(scdb.path(rid))
            rec["id"] = new_id
            existing.add(new_id)
        if scdb.dump(rec) != before or new_id:
            rec["updated"] = scdb.today()
            changed += 1
            if not args.dry_run:
                scdb.save(rec)
    print("%s %d of %d records" % ("would change" if args.dry_run else "changed", changed, len(changes)))


if __name__ == "__main__":
    main()

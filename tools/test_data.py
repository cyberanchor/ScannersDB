#!/usr/bin/env python3
"""Check the data before a commit.

  records        schema, values and networks of every data/scanners/*.yaml (scdb.check) and the canonical format
  overlaps       networks that two records claim (warning only: cloud addresses get reused and some scanners run on
                 another company's scanners); cloud records are not compared
  sources.yaml   rules and mappings point at records that exist
  lists          data/lists/ is what tools/export.py builds from the records
  README         the generated parts of README.md and data/README.md are up to date

usage: python3 tools/test_data.py [--fix]
  --fix   rewrite records that are only off in format (key order, quotes, sorting), then check again

Exit status 1 when something is wrong.
"""
import ipaddress
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scdb  # noqa: E402
import export  # noqa: E402
import readme_table  # noqa: E402


def overlaps(records):
    """{(id_a, id_b): count} of networks shared by two records."""
    rows = []
    for rec in records:
        for fam in (4, 6):
            for n in scdb.nets(rec, fam):
                rows.append((fam, int(n.network_address), int(n.broadcast_address), rec["id"]))
    rows.sort()
    out = {}
    active = []  # (end, id) of earlier networks that may still overlap, per family
    fam_now = None
    for fam, start, end, rid in rows:
        if fam != fam_now:
            active, fam_now = [], fam
        active = [(e, r) for e, r in active if e >= start]
        for e, r in active:
            if r != rid:
                key = tuple(sorted((r, rid)))
                out[key] = out.get(key, 0) + 1
        active.append((end, rid))
    return out


def check_sources(ids):
    p = []
    with open(readme_table.SOURCES, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    for r in config.get("rules") or []:
        for k in ("record", "net", "action", "why"):
            if k not in r:
                p.append("sources.yaml: a rule has no %s: %r" % (k, r))
        for k in ("record", "to"):
            if r.get(k) and r[k] not in ids:
                p.append("sources.yaml: rule %s %s names %r, which is not a record" % (r.get("action"), r.get("net"),
                                                                                       r[k]))
        try:
            ipaddress.ip_network(r.get("net", ""), strict=False)
        except ValueError:
            p.append("sources.yaml: rule network %r is not a network" % r.get("net"))
    for name, src in config["sources"].items():
        for k in ("name", "home", "download", "format", "link"):
            if k not in src:
                p.append("sources.yaml: %s has no %s" % (name, k))
        targets = list((src.get("files") or {}).values()) + list((src.get("only") or {}).values())
        for patterns in (src.get("groups") or {}).values():
            targets += [rid for _, rid in patterns]
        targets += [rid for _, rid in src.get("sections") or []]
        if src.get("record"):
            targets.append(src["record"])
        for rid in sorted(set(targets) - set(ids)):
            p.append("sources.yaml: %s maps to %r, which is not a record" % (name, rid))
    return p


def main():
    fix = "--fix" in sys.argv[1:]
    errors, warnings = [], []
    stray = [f for f in os.listdir(scdb.DIR) if not f.endswith(".yaml")]
    errors += ["data/scanners/%s: not a .yaml record" % f for f in stray]
    records = []
    for rid in scdb.ids():
        try:
            rec = scdb.load(rid)
        except (yaml.YAMLError, ValueError) as e:
            errors.append("%s: cannot be read: %s" % (rid, e))
            continue
        records.append(rec)
        for problem in scdb.check(rec):
            errors.append("%s: %s" % (rid, problem))
        with open(scdb.path(rid), encoding="utf-8") as f:
            text = f.read()
        if text != scdb.dump(rec):
            if fix:
                scdb.save(rec)
            else:
                errors.append("%s: not in the canonical format (run tools/test_data.py --fix)" % rid)
    ids = {r["id"] for r in records}
    names = {}
    for r in records:
        if r.get("name"):
            names.setdefault(r["name"].lower(), []).append(r["id"])
    errors += ["two records named %r: %s" % (n, ", ".join(v)) for n, v in names.items() if len(v) > 1]

    cloud = {r["id"] for r in records if r.get("category") == "cloud"}
    for (a, b), n in sorted(overlaps(records).items()):
        if a in cloud or b in cloud:
            continue    # cloud records are whole provider ranges: scanners inside them are expected
        warnings.append("%s and %s share %d network%s" % (a, b, n, "s" if n > 1 else ""))
    errors += check_sources(ids)

    if not errors:
        files = export.build(scdb.LISTS)
        on_disk = set()
        for base, _, fnames in os.walk(scdb.LISTS):
            for fn in fnames:
                on_disk.add(os.path.relpath(os.path.join(base, fn), scdb.LISTS))
        for rel, text in files.items():
            p = os.path.join(scdb.LISTS, rel)
            if not os.path.exists(p):
                errors.append("data/lists/%s is missing (run tools/export.py)" % rel)
                continue
            with open(p, encoding="utf-8") as f:
                if f.read() != text:
                    errors.append("data/lists/%s is not up to date (run tools/export.py)" % rel)
        errors += ["data/lists/%s is not built from any record (run tools/export.py)" % rel
                   for rel in sorted(on_disk - set(files))]
        for path, parts in ((scdb.README, readme_table.readme_parts(records)),
                            (readme_table.DATA_README, readme_table.data_readme_parts(records))):
            with open(path, encoding="utf-8") as f:
                old = f.read()
            try:
                if readme_table.fill(old, parts, path) != old:
                    errors.append("%s is not up to date (run tools/readme_table.py)" % os.path.relpath(path, scdb.ROOT))
            except SystemExit as e:
                errors.append(str(e))
        links = re.findall(r"\]\((data/scanners/[^)]+)\)", open(scdb.README, encoding="utf-8").read())
        errors += ["README.md links to %s, which does not exist" % l for l in links
                   if not os.path.exists(os.path.join(scdb.ROOT, l))]

    for w in warnings:
        print("warning: " + w)
    for e in errors:
        print("error: " + e)
    total4 = sum(len(scdb.nets(r, 4)) for r in records)
    total6 = sum(len(scdb.nets(r, 6)) for r in records)
    print("%d records, %d IPv4 and %d IPv6 networks: %d errors, %d warnings"
          % (len(records), total4, total6, len(errors), len(warnings)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

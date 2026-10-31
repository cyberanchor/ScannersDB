#!/usr/bin/env python3
"""Write the generated parts of README.md and data/README.md, between <!-- name:start --> and <!-- name:end -->.

  README.md        stats (counts), scanners (active records), inactive, cloud
  data/README.md   sources (from tools/sources.yaml), rules (networks left out or corrected)

Tables are aligned as a monospace editor shows them: emoji and wide characters take two columns.

usage: python3 tools/readme_table.py [--check]     (--check: exit 1 when a file is not up to date, write nothing)
"""
import ipaddress
import os
import re
import sys
import unicodedata
from urllib.parse import urlparse

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scdb  # noqa: E402

DATA_README = os.path.join(scdb.ROOT, "data", "README.md")
SOURCES = os.path.join(scdb.ROOT, "tools", "sources.yaml")
ZERO_WIDTH = {"‍", "︎", "️"}


def flag_width(text):
    """A flag is two regional indicator letters shown as one two-column glyph."""
    n = 0
    chars = list(text)
    i = 0
    while i < len(chars):
        ch = chars[i]
        if 0x1F1E6 <= ord(ch) <= 0x1F1FF and i + 1 < len(chars) and 0x1F1E6 <= ord(chars[i + 1]) <= 0x1F1FF:
            n += 2
            i += 2
            continue
        if unicodedata.combining(ch) or ch in ZERO_WIDTH:
            pass
        elif unicodedata.east_asian_width(ch) in ("W", "F"):
            n += 2
        else:
            n += 1
        i += 1
    return n


def table(header, rows, right=()):
    cells = [header] + rows
    widths = [max(flag_width(r[j]) for r in cells) for j in range(len(header))]
    widths = [max(w, 3) for w in widths]

    def line(r):
        out = []
        for j, c in enumerate(r):
            pad = " " * (widths[j] - flag_width(c))
            out.append(pad + c if j in right else c + pad)
        return "| " + " | ".join(out) + " |"

    sep = "|" + "|".join(("-" * (widths[j] + 1) + ":") if j in right else ("-" * (widths[j] + 2))
                         for j in range(len(header))) + "|"
    return [line(header), sep] + [line(r) for r in rows]


def site(url):
    if not url:
        return ""
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def num(n):
    return "{:,}".format(n)


def record_rows(records):
    rows = []
    for i, r in enumerate(sorted(records, key=lambda x: re.sub(r"^\W+", "", x["name"]).lower()), 1):
        link = "[%s](%s)" % (site(r["website"]), r["website"]) if r.get("website") else "—"
        rows.append([str(i), r["name"].replace("|", "\\|"), link, r.get("flag") or "❓", r["category"],
                     num(len(scdb.nets(r, 4))), "[%s](data/scanners/%s.yaml)" % (r["id"], r["id"])])
    return rows


HEADER = ["#", "Company / resource", "Link", "Flag", "Type", "IPv4", "Record"]


def readme_parts(records):
    import export  # same folder
    main = [r for r in records if export.in_combined(r)]
    inactive = [r for r in records if r.get("status") == "inactive" and r.get("category") != "cloud"]
    cloud = [r for r in records if r.get("category") == "cloud"]
    v4, v6 = export.combined(main, 4), export.combined(main, 6)
    every4 = sum(len(scdb.nets(r, 4)) for r in records)
    every6 = sum(len(scdb.nets(r, 6)) for r in records)
    stamp = max((r.get("updated", "") for r in records), default=scdb.today())
    stats = ["**%d** records (%d active scanners, %d inactive, %d cloud) · **%s** IPv4 and **%s** IPv6 networks in the "
             "records · combined list: **%s** IPv4 networks (%s addresses) and **%s** IPv6 networks · updated %s"
             % (len(records), len(main), len(inactive), len(cloud), num(every4), num(every6), num(len(v4)),
                num(sum(n.num_addresses for n in v4)), num(len(v6)), stamp)]
    return {
        "stats": stats,
        "scanners": table(HEADER, record_rows(main), right=(0, 5)),
        "inactive": table(HEADER, record_rows(inactive), right=(0, 5)),
        "cloud": table(HEADER, record_rows(cloud), right=(0, 5)),
    }


def data_readme_parts(records):
    with open(SOURCES, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    feeds = {}
    for rec in records:
        for s in rec.get("sources") or []:
            feeds.setdefault(s, set()).add(rec["id"])
    rows = []
    for name, src in config["sources"].items():
        prefix = src["link"].split("{")[0]
        count = len({rid for link, rids in feeds.items() if link.startswith(prefix) for rid in rids})
        rows.append(["[%s](%s)" % (src["name"], src["home"]), src.get("license", "—"), src["format"], str(count)])
    sources = table(["Source", "License", "Read as", "Records"], rows, right=(3,))
    rule_rows = []
    for r in config.get("rules") or []:
        if r["action"] == "move":
            what = "moved to %s" % r.get("to")
        elif r["action"] == "replace":
            what = "written as %s" % ", ".join(r["with"] if isinstance(r["with"], list) else [r["with"]])
        else:
            what = "left out"
        rule_rows.append([r["record"], scdb.fmt(ipaddress.ip_network(r["net"], strict=False)), r.get("source", "any"),
                          what, r["why"].replace("|", "\\|")])
    rules = table(["Record", "Network", "Source", "Action", "Why"], rule_rows)
    return {"sources": sources, "rules": rules}


def fill(text, parts, path):
    for name, block in parts.items():
        start, end = "<!-- %s:start -->" % name, "<!-- %s:end -->" % name
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
        if not pattern.search(text):
            raise SystemExit("%s: markers %s ... %s not found" % (path, start, end))
        text = pattern.sub(lambda m: start + "\n" + "\n".join(block) + "\n" + end, text)
    return text


def main():
    check = "--check" in sys.argv[1:]
    records = scdb.load_all()
    stale = []
    for path, parts in ((scdb.README, readme_parts(records)), (DATA_README, data_readme_parts(records))):
        with open(path, encoding="utf-8") as f:
            old = f.read()
        new = fill(old, parts, path)
        if new != old:
            stale.append(os.path.relpath(path, scdb.ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    if check:
        if stale:
            print("not up to date: %s (run tools/readme_table.py)" % ", ".join(stale))
            sys.exit(1)
        print("README tables are up to date")
    else:
        print("updated: %s" % (", ".join(stale) or "nothing"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Download the upstream scanner lists named in tools/sources.yaml and merge them into data/scanners/.

The merge only adds. Networks that no upstream list has any more stay in the records and are listed in the
report, so networks added by hand are never lost. Networks an upstream list puts under the wrong organisation
are handled by the rules at the end of sources.yaml.

usage: python3 tools/import_sources.py [--apply] [--offline] [--no-lookup] [--only SOURCE,...]

  without --apply   download, compare and write the report; the records are not changed
  --apply           add the new networks, and new records for lists that have none yet
  --offline         read the downloads of the previous run (~/.cache/scannersdb/src/) instead of downloading
  --no-lookup       do not ask ip-api.com for network owners; new networks go to a block without owner
                    (fill it later with tools/enrich.py)
  --only            use only these sources (comma separated names from sources.yaml); nothing is reported
                    as missing upstream then, and provenance.json is left as it was

Report: ~/.cache/scannersdb/review.md. Which source lists each network: ~/.cache/scannersdb/provenance.json
(read by tools/where.py).
"""
import argparse
import bisect
import fnmatch
import io
import ipaddress
import json
import os
import re
import sys
import tarfile
import urllib.request

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scdb  # noqa: E402

CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources.yaml")
NET_RE = re.compile(r"^[0-9A-Fa-f:.]+(?:/\d{1,3})?$")


class Item:
    __slots__ = ("source", "ref", "rid", "net", "label")

    def __init__(self, source, ref, rid, net, label=None):
        self.source, self.ref, self.rid, self.net, self.label = source, ref, rid, net, label


class Collector:
    def __init__(self):
        self.items = []
        self.meta = {}          # rid -> {"names": [...], "inactive": bool, "active": bool, "links": [(source, link)]}
        self.warnings = []
        self.lists = {}         # source -> number of lists read

    def add(self, source, ref, rid, text, label=None, link=None, name=None, inactive=False):
        text = text.strip()
        if not text:
            return
        if not NET_RE.match(text):
            self.warnings.append("%s %s: not a network: %r" % (source, ref, text))
            return
        try:
            net, _ = scdb.parse_net(text)
        except ValueError:
            self.warnings.append("%s %s: not a network: %r" % (source, ref, text))
            return
        try:
            ipaddress.ip_network(text)
        except ValueError:
            self.warnings.append("%s %s: host bits set in %s, read as %s" % (source, ref, text, scdb.fmt(net)))
        if not net.is_global or net.is_multicast:
            self.warnings.append("%s %s: not a public network: %s" % (source, ref, text))
            return
        self.items.append(Item(source, ref, rid, net, label))
        m = self.meta.setdefault(rid, {"names": [], "inactive": False, "active": False, "links": []})
        if name and name not in m["names"]:
            m["names"].append(name)
        if inactive:
            m["inactive"] = True
        else:
            m["active"] = True
        if link and (source, link) not in m["links"]:
            m["links"].append((source, link))


# --- download -------------------------------------------------------------------------------------------------

def fetch(url, dest, offline):
    if offline:
        with open(dest, "rb") as f:
            return f.read()
    req = urllib.request.Request(url, headers={"User-Agent": scdb.UA})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    return data


def downloads(name, src, offline):
    """{key: bytes} for one source; key is the download name (or "main" when there is one download)."""
    urls = src["download"]
    if isinstance(urls, str):
        urls = {"main": urls}
    out = {}
    for key, url in urls.items():
        ext = ".tar.gz" if "codeload.github.com" in url else os.path.splitext(url.split("?")[0])[1] or ".txt"
        out[key] = fetch(url, os.path.join(scdb.CACHE, "src", name, key + ext), offline)
    return out


def read_tar(data):
    """{path inside the archive, without the top folder: text} for the .nft and .txt files of a .tar.gz.

    Files are read in memory; nothing from the archive is written to disk."""
    out = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for m in tar:
            if not m.isfile() or m.size > 50 << 20:
                continue
            name = m.name.split("/", 1)[1] if "/" in m.name else m.name
            if name.endswith((".nft", ".txt")):
                out[name] = tar.extractfile(m).read().decode("utf-8", "replace")
    return out


# --- formats --------------------------------------------------------------------------------------------------

def match_label(patterns, label):
    low = re.sub(r"\s+", " ", (label or "").lower())
    for pattern, rid in patterns:
        if pattern.lower() in low:
            return rid
    return None


def header_name(header):
    """Organisation name from the first comment line of an OpenFilters file: 'Censys (censys.io / ...)'."""
    if not header:
        return None
    return re.sub(r"\s*\(.*$", "", header[0]).strip() or None


def parse_openfilters(c, name, src, data):
    files = read_tar(data["main"])
    mapping = src.get("files") or {}
    groups = src.get("groups") or {}
    for path, text in sorted(files.items()):
        m = re.match(r"^(inactive/)?([^/]+)\.nft$", path)
        if not m:
            continue
        inactive, stem = bool(m.group(1)), m.group(2)
        c.lists[name] = c.lists.get(name, 0) + 1
        header, family, label, seen_define = [], None, None, False
        link = src["link"].format(file=path)
        for line in text.splitlines():
            s = line.strip()
            if not s:
                continue
            if s.startswith("define "):
                seen_define, label = True, None
                family = 6 if re.search(r"_v6\b", s) else 4
                continue
            if family is None:
                if s.startswith("#") and not seen_define:
                    header.append(s.lstrip("#").strip())
                continue
            if s.startswith("}"):
                family = None
                continue
            if s.startswith("#"):
                label = s.lstrip("#").strip()
                continue
            for entry in s.rstrip(",").split(","):
                entry = entry.strip().rstrip("}").strip()
                if not entry:
                    continue
                if stem in groups:
                    rid = match_label(groups[stem], label)
                    if not rid:
                        c.warnings.append("%s %s: no record for the group %r (%s)" % (name, path, label, entry))
                        continue
                    c.add(name, path, rid, entry, label=label, link=link, name=label, inactive=inactive)
                else:
                    rid = mapping.get(stem, stem)
                    c.add(name, path, rid, entry, label=label, link=link, name=header_name(header),
                          inactive=inactive)


def plain_lines(text):
    """(entry, last comment) for every network line of a plain list; comments after an entry are dropped."""
    label = None
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            label = s.lstrip("#").strip()
            continue
        yield s.split("#", 1)[0].split()[0], label


def parse_lists(c, name, src, data):
    if "main" in data and data["main"][:2] == b"\x1f\x8b":
        files = read_tar(data["main"])
        mapping = src.get("files") or {}
        only = src.get("only")
        for path, text in sorted(files.items()):
            if only is not None:
                if path not in only:
                    continue
                rid = only[path]
            else:
                if "/" in path or not path.endswith(".txt"):
                    continue
                stem = path[:-4]
                rid = mapping.get(stem, stem)
            c.lists[name] = c.lists.get(name, 0) + 1
            link = src["link"].format(file=path)
            for entry, label in plain_lines(text):
                c.add(name, path, rid, entry, label=label, link=link)
        return
    for key, raw in data.items():
        rid = src.get("record") or key
        c.lists[name] = c.lists.get(name, 0) + 1
        link = src["link"].format(file=key)
        for entry, label in plain_lines(raw.decode("utf-8", "replace")):
            c.add(name, key, rid, entry, label=label, link=link)


def parse_sections(c, name, src, data):
    text = data["main"].decode("utf-8", "replace")
    patterns = src["sections"]
    label, started = None, False
    c.lists[name] = 1
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            body = s.strip("#").strip()
            if s.startswith("# ---"):
                started = True
            if started and body:
                label = body.strip("- ").strip()
            continue
        rid = match_label(patterns, label)
        if not rid:
            c.warnings.append("%s: no record for the section %r (%s)" % (name, label, s))
            continue
        c.add(name, label, rid, s.split("#", 1)[0].strip(), label=label, link=src["link"])


def json_path(obj, path):
    parts = path.split(".")
    values = [obj]
    for part in parts:
        many = part.endswith("[]")
        key = part[:-2] if many else part
        nxt = []
        for v in values:
            v = v.get(key) if isinstance(v, dict) else None
            if v is None:
                continue
            if many:
                nxt.extend(v if isinstance(v, list) else [])
            else:
                nxt.append(v)
        values = nxt
    out = []
    for v in values:
        out.extend(v if isinstance(v, list) else [v])
    return [v for v in out if isinstance(v, str)]


def parse_json(c, name, src, data):
    for key, raw in data.items():
        obj = json.loads(raw.decode("utf-8", "replace"))
        c.lists[name] = c.lists.get(name, 0) + 1
        for path in src["paths"]:
            for entry in json_path(obj, path):
                c.add(name, key, src["record"], entry, link=src["link"])


PARSERS = {"openfilters": parse_openfilters, "lists": parse_lists, "sections": parse_sections, "json": parse_json}


# --- merge ----------------------------------------------------------------------------------------------------

class Cover:
    """Fast 'is this network inside the union of these networks' test."""

    def __init__(self, networks):
        merged = sorted(ipaddress.collapse_addresses(networks), key=scdb.sort_key) if networks else []
        self.starts = [int(n.network_address) for n in merged]
        self.ends = [int(n.broadcast_address) for n in merged]

    def __contains__(self, net):
        i = bisect.bisect_right(self.starts, int(net.network_address)) - 1
        return i >= 0 and int(net.broadcast_address) <= self.ends[i]


def apply_rules(c, rules):
    """drop: leave the network out; move: put it into record `to`; replace: use the networks `with` instead
    (for lists with a wrong prefix length). Returns (rule, item) for every network a rule touched."""
    hits = []
    kept = []
    parsed = [(r, ipaddress.ip_network(r["net"], strict=False)) for r in rules]
    for r, _ in parsed:
        if r.get("action") not in ("drop", "move", "replace"):
            sys.exit("sources.yaml: rule for %s has an unknown action %r" % (r.get("record"), r.get("action")))
    for it in c.items:
        for r, rnet in parsed:
            if it.rid != r["record"] or it.net.version != rnet.version or not it.net.subnet_of(rnet):
                continue
            if r.get("source") and not fnmatch.fnmatch(it.source, r["source"]):
                continue
            hits.append((r, it))
            if r["action"] == "move":
                it.rid = r["to"]
                m = c.meta.setdefault(it.rid, {"names": [], "inactive": False, "active": True, "links": []})
                link = next((lk for s, lk in c.meta.get(r["record"], {}).get("links", []) if s == it.source), None)
                if link and (it.source, link) not in m["links"]:
                    m["links"].append((it.source, link))
                kept.append(it)
            elif r["action"] == "replace":
                with_ = r["with"] if isinstance(r["with"], list) else [r["with"]]
                for text in with_:
                    kept.append(Item(it.source, it.ref, it.rid, ipaddress.ip_network(text), it.label))
            break
        else:
            kept.append(it)
    c.items = kept
    return hits


def rule_lines(hits):
    """Report lines, one per rule and source: the networks a rule touched are listed together."""
    grouped = {}
    for r, it in hits:
        grouped.setdefault((id(r), it.source), (r, []))[1].append(it.net)
    out = []
    for (_, source), (r, networks) in grouped.items():
        networks = scdb.remove_subsumed(networks)
        shown = ", ".join(scdb.fmt(n) for n in networks[:6]) + (" ..." if len(networks) > 6 else "")
        target = {"move": " -> " + str(r.get("to")), "replace": " -> " + str(r.get("with"))}.get(r["action"], "")
        out.append("- %s %s from %s: %s%s (%s)" % (r["action"], r["record"], source, shown, target, r["why"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--no-lookup", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()

    with open(CONFIG, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    order = list(config["sources"])
    chosen = order if not args.only else [s.strip() for s in args.only.split(",")]
    for s in chosen:
        if s not in config["sources"]:
            sys.exit("unknown source %r; sources.yaml has: %s" % (s, ", ".join(order)))

    c = Collector()
    for name in chosen:
        src = config["sources"][name]
        print("%-16s %s" % (name, "cached" if args.offline else "downloading"), file=sys.stderr)
        try:
            data = downloads(name, src, args.offline)
        except Exception as e:  # one source down must not stop the others
            c.warnings.append("%s: download failed: %s" % (name, e))
            continue
        PARSERS[src["format"]](c, name, src, data)

    hits = apply_rules(c, config.get("rules") or [])

    # rid -> family -> network -> sources
    cands = {}
    for it in c.items:
        cands.setdefault(it.rid, {}).setdefault(it.net.version, {}).setdefault(it.net, set()).add(it.source)

    existing = set(scdb.ids())
    report_new, report_added, report_gone, provenance = [], [], [], {}
    plan = []           # (rid, rec, meta, {fam: new networks})
    for rid in sorted(cands):
        fams = cands[rid]
        meta = c.meta.get(rid, {"names": [], "inactive": False, "active": True, "links": []})
        if rid in existing:
            rec = scdb.load(rid)
        else:
            rec = {"id": rid, "name": (meta["names"] or [rid])[0], "category": "unknown",
                   "status": "inactive" if meta["inactive"] and not meta["active"] else "active"}
            report_new.append(rid)
        provenance[rid] = {}
        news = {}
        for fam in (4, 6):
            upstream = fams.get(fam, {})
            for n, s in upstream.items():
                provenance[rid][scdb.fmt(n)] = sorted(s, key=order.index)
            have = scdb.nets(rec, fam)
            have_cover = Cover(have)
            new = [n for n in upstream if n not in have_cover]
            if new:
                news[fam] = new
                report_added.append((rid, fam, scdb.remove_subsumed(new)))
            if not args.only and have:
                up_cover = Cover(list(upstream))
                gone = [n for n in have if n not in up_cover]
                if gone:
                    report_gone.append((rid, fam, gone))
        plan.append((rid, rec, meta, news))

    if args.apply and not args.no_lookup:
        # one pass over ip-api.com for every network that will need an owner, so the per-record rebuilds below
        # find all answers in the cache
        wanted = []
        for rid, rec, meta, news in plan:
            for fam, new in news.items():
                known = scdb.block_info(rec, fam)
                for n in scdb.remove_subsumed(scdb.nets(rec, fam) + new):
                    if not known.get(scdb.fmt(n)):
                        wanted.append(str(n.network_address))
        if wanted:
            print("looking up %d networks at ip-api.com" % len(set(wanted)), file=sys.stderr)
            scdb.lookup(sorted(set(wanted), key=lambda a: ipaddress.ip_address(a).packed))

    changed = 0
    for rid, rec, meta, news in plan:
        touched = False
        if args.apply and rid in existing:
            rec = scdb.load(rid)    # read again: the lookups can take long and the file may have been edited meanwhile
        if args.apply:
            for fam, new in news.items():
                scdb.rebuild(rec, fam, new=new, offline=args.no_lookup)
                touched = True
        links = [lk for s, lk in sorted(meta["links"], key=lambda x: order.index(x[0]))]
        sources = list(rec.get("sources") or [])
        for lk in links:
            if lk not in sources:
                sources.append(lk)
                touched = True
        rec["sources"] = sources
        if args.apply and (touched or rid not in existing):
            rec["updated"] = scdb.today()
            scdb.save(rec)
            changed += 1

    # records no upstream list mentions (only reported)
    untouched = sorted(existing - set(cands)) if not args.only else []

    os.makedirs(scdb.CACHE, exist_ok=True)
    if not args.only:   # a partial run would leave out what the other sources list
        with open(os.path.join(scdb.CACHE, "provenance.json"), "w", encoding="utf-8") as f:
            json.dump(provenance, f, indent=0, sort_keys=True)
    lines = ["# ScannersDB import report (%s)" % scdb.today(), "",
             "Mode: %s%s" % ("apply" if args.apply else "compare only (run with --apply to write)",
                             ", sources: " + ", ".join(chosen) if args.only else ""), "",
             "## Sources", "", "| Source | Lists | Networks |", "|---|---|---|"]
    per_source = {}
    for it in c.items:
        per_source[it.source] = per_source.get(it.source, 0) + 1
    for name in chosen:
        lines.append("| %s | %d | %d |" % (name, c.lists.get(name, 0), per_source.get(name, 0)))
    lines += ["", "## New records (%d)" % len(report_new), ""] + ["- %s" % r for r in report_new]
    lines += ["", "## New networks", ""]
    for rid, fam, new in report_added:
        lines.append("- %s IPv%d: %d new: %s" % (rid, fam, len(new), ", ".join(scdb.fmt(n) for n in new[:20])
                                               + (" ..." if len(new) > 20 else "")))
    lines += ["", "## In the records but in no upstream list (kept)", ""]
    for rid, fam, gone in report_gone:
        lines.append("- %s IPv%d: %d: %s" % (rid, fam, len(gone), ", ".join(scdb.fmt(n) for n in gone[:30])
                                           + (" ..." if len(gone) > 30 else "")))
    if untouched:
        lines += ["", "## Records no upstream list feeds", ""] + ["- %s" % r for r in untouched]
    lines += ["", "## Rules applied (%d networks)" % len(hits), ""] + rule_lines(hits)
    lines += ["", "## Warnings (%d)" % len(c.warnings), ""] + ["- %s" % w for w in c.warnings]
    report = os.path.join(scdb.CACHE, "review.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("networks read: %d, records: %d (new: %d), records with new networks: %d, changed files: %d"
          % (len(c.items), len(cands), len(report_new), len({r for r, _, _ in report_added}), changed))
    print("warnings: %d, rules applied: %d; report: %s" % (len(c.warnings), len(hits), report))


if __name__ == "__main__":
    main()

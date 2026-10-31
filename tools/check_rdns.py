#!/usr/bin/env python3
"""Check the reverse DNS (PTR) of single addresses against the `rdns` patterns of their record.

Scanner addresses on cloud servers are given to other customers once the scanner lets them go. A PTR that now names
a different, specific host is a hint that an address is stale; no PTR or a generic cloud PTR proves nothing.
The script only reports, it changes no record.

usage: python3 tools/check_rdns.py [--workers N] [--limit N] [ID ...]

  ID          records to check (default: every record with rdns patterns)
  --limit     check at most N addresses per record (a sample, for big records)

Report: ~/.cache/scannersdb/rdns.md. Per record: addresses whose PTR matches, has another name, or has none.
"""
import argparse
import concurrent.futures
import fnmatch
import ipaddress
import os
import socket
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scdb  # noqa: E402

GENERIC = ("amazonaws.com", "googleusercontent.com", "cloudapp.azure.com", "linodeusercontent.com", "vultrusercontent.com",
           "your-server.de", "static.", "in-addr.arpa", "ip6.arpa", "unassigned", "dynamic", "hostingservers",
           "digitalocean", "clients.", "rev.", "ptr.", "reverse", "ovh.net", "contaboserver.net")


def ptr(addr):
    try:
        return socket.gethostbyaddr(addr)[0].lower().rstrip(".")
    except (socket.herror, socket.gaierror, OSError):
        return ""


def matches(name, patterns):
    for p in patterns:
        p = p.lower().rstrip(".")
        if fnmatch.fnmatch(name, p) or (p.startswith("*.") and name == p[2:]):
            return True
        if "*" not in p and "[" not in p and name == p:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--workers", type=int, default=48)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    socket.setdefaulttimeout(5)
    records = [scdb.load(r) for r in (args.ids or scdb.ids())]
    records = [r for r in records if r.get("rdns")]
    jobs = []
    for rec in records:
        singles = [n for fam in (4, 6) for n in scdb.nets(rec, fam) if n.prefixlen == n.max_prefixlen]
        if args.limit:
            singles = singles[:args.limit]
        jobs.extend((rec["id"], str(n.network_address)) for n in singles)
    print("checking %d addresses of %d records" % (len(jobs), len(records)), file=sys.stderr)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        names = list(pool.map(lambda j: ptr(j[1]), jobs))
    by_rec = {}
    for (rid, addr), name in zip(jobs, names):
        by_rec.setdefault(rid, []).append((addr, name))
    lines = ["# ScannersDB reverse DNS check (%s)" % scdb.today(), "",
             "| Record | Checked | PTR matches | Other specific name | Generic name | No PTR |", "|---|---|---|---|---|---|"]
    details = []
    for rec in records:
        rows = by_rec.get(rec["id"], [])
        if not rows:
            continue
        ok = [a for a, n in rows if n and matches(n, rec["rdns"])]
        none = [a for a, n in rows if not n]
        generic = [(a, n) for a, n in rows if n and not matches(n, rec["rdns"]) and any(g in n for g in GENERIC)]
        other = [(a, n) for a, n in rows if n and not matches(n, rec["rdns"]) and not any(g in n for g in GENERIC)]
        lines.append("| %s | %d | %d | %d | %d | %d |" % (rec["id"], len(rows), len(ok), len(other), len(generic),
                                                         len(none)))
        if other:
            details.append("## %s: other names (%s)" % (rec["id"], ", ".join(rec["rdns"])))
            details.append("")
            details.extend("- %s %s" % (a, n) for a, n in sorted(
                other, key=lambda x: (ipaddress.ip_address(x[0]).version, int(ipaddress.ip_address(x[0])))))
            details.append("")
    os.makedirs(scdb.CACHE, exist_ok=True)
    report = os.path.join(scdb.CACHE, "rdns.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write("\n".join(lines + [""] + details) + "\n")
    print("\n".join(lines))
    print("details: %s" % report)


if __name__ == "__main__":
    main()

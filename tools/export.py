#!/usr/bin/env python3
"""Build the ready-to-use lists in data/lists/ from data/scanners/.

  scanners_v4.txt, scanners_v6.txt   every active record except category cloud, merged into the fewest networks
  scanners.nft                       the same as an nftables table that drops them (nft -f scanners.nft)
  scanners.ipset                     the same for ipset restore (sets scannersdb_v4 / scannersdb_v6)
  cloud_v4.txt, cloud_v6.txt         the cloud records only (whole provider ranges, use with care)
  v4/<id>.txt, v6/<id>.txt           one list per record, inactive and cloud records too
  scanners.csv                       one row per network with the record and network owner fields
  scanners.json                      every record with its fields and counts

Plain lists hold one network per line and no comments, so ipset, nft, firewalld and most tools read them as is.

usage: python3 tools/export.py [OUTDIR]     (default data/lists)
"""
import csv
import io
import ipaddress
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scdb  # noqa: E402

CSV_FIELDS = ["id", "name", "legal_entity", "country", "category", "status", "family", "network", "asn", "isp",
              "org", "network_country"]


def combined(records, fam):
    networks = []
    for rec in records:
        networks.extend(scdb.nets(rec, fam))
    return sorted(ipaddress.collapse_addresses(networks), key=scdb.sort_key) if networks else []


def lines(networks):
    return "".join(scdb.fmt(n) + "\n" for n in networks)


def in_combined(rec):
    return rec.get("status") == "active" and rec.get("category") != "cloud"


def nft_text(v4, v6, stamp, count):
    def elements(nets):
        if not nets:
            return ""
        body = ",\n".join("\t\t\t" + scdb.fmt(n) for n in nets)
        return "\t\telements = {\n%s\n\t\t}\n" % body

    return (
        "#!/usr/sbin/nft -f\n"
        "# ScannersDB %s: %d records, %d IPv4 and %d IPv6 networks (cloud ranges and inactive records left out).\n"
        "# %s\n"
        "# Load: nft -f scanners.nft (again to update). Remove: nft delete table inet scannersdb\n"
        "# The input chain drops new connections from the listed networks; add a forward chain the same way on a\n"
        "# router.\n\n"
        "table inet scannersdb\n"
        "delete table inet scannersdb\n\n"
        "table inet scannersdb {\n"
        "\tset scanners_v4 {\n\t\ttype ipv4_addr\n\t\tflags interval\n\t\tauto-merge\n%s\t}\n\n"
        "\tset scanners_v6 {\n\t\ttype ipv6_addr\n\t\tflags interval\n\t\tauto-merge\n%s\t}\n\n"
        "\tchain input {\n"
        "\t\ttype filter hook input priority filter - 10; policy accept;\n"
        "\t\tip saddr @scanners_v4 counter drop\n"
        "\t\tip6 saddr @scanners_v6 counter drop\n"
        "\t}\n"
        "}\n" % (stamp, count, len(v4), len(v6), scdb.REPO, elements(v4), elements(v6)))


# Fixed set sizes, so a later file creates the sets with the same options and `ipset restore -exist` accepts it.
IPSET = {4: ("scannersdb_v4", "inet", 16384, 262144), 6: ("scannersdb_v6", "inet6", 4096, 65536)}


def ipset_text(v4, v6, stamp, count):
    out = io.StringIO()
    out.write("# ScannersDB %s: %d records, %d IPv4 and %d IPv6 networks. %s\n" % (stamp, count, len(v4), len(v6),
                                                                                  scdb.REPO))
    out.write("# Load (again to update): ipset restore -exist < scanners.ipset, then once for example\n")
    out.write("#   iptables -I INPUT -m set --match-set scannersdb_v4 src -j DROP\n")
    out.write("#   ip6tables -I INPUT -m set --match-set scannersdb_v6 src -j DROP\n")
    out.write("# The new entries go into a temporary set that is swapped in, so the set is never empty while loading.\n")
    for fam, nets in ((4, v4), (6, v6)):
        name, family, hashsize, maxelem = IPSET[fam]
        if len(nets) > maxelem:
            raise SystemExit("export: %d IPv%d networks do not fit ipset maxelem %d" % (len(nets), fam, maxelem))
        opts = "hash:net family %s hashsize %d maxelem %d" % (family, hashsize, maxelem)
        out.write("create %s %s\n" % (name, opts))
        out.write("create %s_new %s\n" % (name, opts))
        out.write("flush %s_new\n" % name)
        for n in nets:
            out.write("add %s_new %s\n" % (name, scdb.fmt(n)))
        out.write("swap %s_new %s\n" % (name, name))
        out.write("destroy %s_new\n" % name)
    return out.getvalue()


def csv_text(records):
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(CSV_FIELDS)
    for rec in records:
        for fam in (4, 6):
            for block in rec.get("ipv%d" % fam) or []:
                for text in block["ip"]:
                    w.writerow([rec["id"], rec.get("name", ""), rec.get("legal_entity", ""), rec.get("country", ""),
                                rec.get("category", ""), rec.get("status", ""), "ipv%d" % fam, text,
                                block.get("asn", ""), block.get("isp", ""), block.get("org", ""),
                                block.get("country", "")])
    return out.getvalue()


def json_text(records):
    out = []
    for rec in records:
        item = {"id": rec["id"]}
        item.update(scdb.canonical(rec))
        for fam in (4, 6):
            networks = scdb.nets(rec, fam)
            item["ipv%d_networks" % fam] = len(networks)
            item["ipv%d_addresses" % fam] = scdb.address_count(networks)
        out.append(item)
    return json.dumps(out, ensure_ascii=False, indent=1) + "\n"


def build(outdir):
    """{relative path: text} of every list."""
    records = scdb.load_all()
    files = {}
    stamp = max((r.get("updated", "") for r in records), default=scdb.today())
    main = [r for r in records if in_combined(r)]
    cloud = [r for r in records if r.get("category") == "cloud"]
    v4, v6 = combined(main, 4), combined(main, 6)
    files["scanners_v4.txt"] = lines(v4)
    files["scanners_v6.txt"] = lines(v6)
    files["scanners.nft"] = nft_text(v4, v6, stamp, len(main))
    files["scanners.ipset"] = ipset_text(v4, v6, stamp, len(main))
    files["cloud_v4.txt"] = lines(combined(cloud, 4))
    files["cloud_v6.txt"] = lines(combined(cloud, 6))
    for rec in records:
        for fam in (4, 6):
            networks = sorted(scdb.nets(rec, fam), key=scdb.sort_key)
            if networks:
                files["v%d/%s.txt" % (fam, rec["id"])] = lines(networks)
    files["scanners.csv"] = csv_text(records)
    files["scanners.json"] = json_text(records)
    return files


def write(outdir, files):
    for sub in ("v4", "v6"):
        shutil.rmtree(os.path.join(outdir, sub), ignore_errors=True)
    for rel, text in files.items():
        p = os.path.join(outdir, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else scdb.LISTS
    files = build(outdir)
    write(outdir, files)
    v4 = files["scanners_v4.txt"].count("\n")
    v6 = files["scanners_v6.txt"].count("\n")
    print("wrote %d files to %s; combined list: %d IPv4 and %d IPv6 networks" % (len(files), outdir, v4, v6))


if __name__ == "__main__":
    main()

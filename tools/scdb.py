#!/usr/bin/env python3
"""ScannersDB records: data/scanners/<id>.yaml, one file per company or scanner.

Every tool reads and writes the records through this module, so all files keep one format.
The fields are described in data/README.md.

    load_all()                   -> records sorted by id; rec["id"] is the file name without .yaml
    load(rid)                    -> one record
    save(rec)                    -> writes the record in the canonical format
    dump(rec)                    -> canonical text of a record
    check(rec)                   -> list of problems found in one record
    nets(rec, fam)               -> every network of the record (fam 4 or 6) as ipaddress objects
    rebuild(rec, fam, new, ...)  -> add networks to a record and regroup its blocks by network owner
    lookup(addresses)            -> {address: {asn, isp, org, country}} from ip-api.com, cached

SCDB_DATA_DIR=/other/folder points the tools at a copy of the records, SCDB_CACHE at another cache.
"""
import datetime
import glob
import ipaddress
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.environ.get("SCDB_DATA_DIR") or os.path.join(ROOT, "data", "scanners")
LISTS = os.path.join(ROOT, "data", "lists")
README = os.path.join(ROOT, "README.md")
CACHE = os.environ.get("SCDB_CACHE") or os.path.join(os.path.expanduser("~"), ".cache", "scannersdb")
REPO = "https://github.com/cyberanchor/ScannersDB"
RAW = "https://raw.githubusercontent.com/cyberanchor/ScannersDB/main"
UA = "ScannersDB/1.0 (+%s)" % REPO

HEAD = "# ScannersDB record; fields are described in data/README.md\n"
# key order in the files
KEYS = ["name", "legal_entity", "flag", "country", "website", "category", "status", "asn", "rdns",
        "user_agents", "opt_out", "note", "ipv4", "ipv6", "sources", "updated"]
REQUIRED = ["name", "category", "status", "sources"]
BLOCK = ["asn", "isp", "org", "country", "ip"]
INFO = ["asn", "isp", "org", "country"]
STATUSES = ("active", "inactive")
CATEGORIES = {
    "search-engine": "Search engine for hosts and services (Shodan, Censys, FOFA ...)",
    "company": "Company scanning for its own products: attack surface, security ratings, threat intelligence, IP data",
    "research": "Research project, non-profit or measurement study",
    "university": "University or research institute",
    "government": "Government agency or national CERT",
    "hobby": "Private or hobby project (game server lists, personal scanners)",
    "unknown": "The operator does not say who it is",
    "cloud": "Whole cloud ranges, not only scanners. Left out of the combined lists",
}
# Shortest prefix accepted in a record: anything wider is almost certainly a typo.
WIDEST = {4: 8, 6: 24}

# One-line strings written in quotes although PyYAML would leave them plain: everything a YAML 1.2 parser might
# read as a number, boolean or null. Over-quoting is harmless, so any text that starts like a number is quoted,
# which covers every IP address, network and date.
QUOTE = re.compile(r"^(?:[-+]?\.?[0-9]|[-+]?\.(?:inf|Inf|INF|nan|NaN|NAN)$"
                   r"|(?:null|Null|NULL|~|true|True|TRUE|false|False|FALSE)$)")
ODD_BREAKS = ("\x85", " ", " ", "\r")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ASN = re.compile(r"^AS[1-9][0-9]{0,9}$")
URL = re.compile(r"^https?://[^\s]+$")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$")


class _Flow(list):
    """A list written on one line: [AS1, AS2]."""


class _Dumper(yaml.SafeDumper):
    pass


def _str(dumper, s):
    if any(c in s for c in ODD_BREAKS):
        return dumper.represent_scalar("tag:yaml.org,2002:str", s, style='"')
    if "\n" in s:
        return dumper.represent_scalar("tag:yaml.org,2002:str", s, style="|")
    if QUOTE.match(s):
        return dumper.represent_scalar("tag:yaml.org,2002:str", s, style="'")
    return dumper.represent_scalar("tag:yaml.org,2002:str", s)


_Dumper.add_representer(str, _str)
_Dumper.add_representer(_Flow, lambda d, v: d.represent_sequence("tag:yaml.org,2002:seq", v, flow_style=True))
_Dumper.add_representer(dict, lambda d, m: d.represent_mapping("tag:yaml.org,2002:map", m.items()))


def today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def path(rid):
    return os.path.join(DIR, rid + ".yaml")


def ids():
    return sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(DIR, "*.yaml")))


def load(rid):
    with open(path(rid), encoding="utf-8") as f:
        rec = yaml.safe_load(f) or {}
    if not isinstance(rec, dict):
        raise ValueError("%s: the file is not a mapping" % path(rid))
    rec["id"] = rid
    return rec


def load_all():
    return [load(rid) for rid in ids()]


# --- networks -------------------------------------------------------------------------------------------------

def parse_net(text):
    """Network from a line of a list: '1.2.3.4', '1.2.3.0/24', '2001:db8::/32'. Host bits are cleared.

    Returns (network, fixed) where fixed tells that the text had host bits set or was not canonical."""
    net = ipaddress.ip_network(text.strip(), strict=False)
    return net, fmt(net) != text.strip()


def fmt(net):
    """Canonical text of a network: a single address is written without /32 or /128."""
    if net.prefixlen == net.max_prefixlen:
        return str(net.network_address)
    return str(net)


def sort_key(net):
    return (net.version, int(net.network_address), net.prefixlen)


def remove_subsumed(networks):
    """Drop duplicates and networks that lie inside another one of the list (CIDR blocks nest or are disjoint)."""
    out = []
    for n in sorted(set(networks), key=sort_key):
        if out and out[-1].version == n.version and n.subnet_of(out[-1]):
            continue
        out.append(n)
    return out


def nets(rec, fam):
    out = []
    for block in rec.get("ipv%d" % fam) or []:
        for text in block.get("ip") or []:
            out.append(ipaddress.ip_network(text))
    return out


def address_count(networks):
    return sum(n.num_addresses for n in remove_subsumed(networks))


def block_info(rec, fam):
    """{network text: {asn, isp, org, country}} as the record has it now."""
    out = {}
    for block in rec.get("ipv%d" % fam) or []:
        info = {k: block[k] for k in INFO if block.get(k)}
        for text in block.get("ip") or []:
            out[text] = info
    return out


def _block_key(b):
    asn = int(b["asn"][2:]) if b.get("asn") else 1 << 40
    return (asn, b.get("country", ""), _norm(b.get("isp", "")), _norm(b.get("org", "")))


def _norm(text):
    return re.sub(r"[^0-9a-z]+", "", (text or "").lower())


def make_blocks(networks, info_for):
    """Group networks by owner (asn, isp, org, country); networks inside one group are merged when adjacent.

    info_for(net) gives the owner of a network: a dict with any of asn / isp / org / country. Names that differ only
    in case or punctuation ("Censys Inc" / "Censys, Inc.") are one owner, written as most of its networks have it."""
    groups = {}
    for n in remove_subsumed(networks):
        info = info_for(n) or {}
        key = tuple(_norm(info.get(k, "")) if k in ("isp", "org") else info.get(k, "") for k in INFO)
        groups.setdefault(key, []).append((n, info))
    blocks = []
    for members in groups.values():
        block = {}
        for k in INFO:
            spellings = {}
            for _, info in members:
                if info.get(k):
                    spellings[info[k]] = spellings.get(info[k], 0) + 1
            if spellings:
                block[k] = max(spellings, key=lambda s: (spellings[s], len(s), s))
        merged = sorted(ipaddress.collapse_addresses([n for n, _ in members]), key=sort_key)
        block["ip"] = [fmt(n) for n in merged]
        blocks.append(block)
    blocks.sort(key=_block_key)
    return blocks


def rebuild(rec, fam, new=(), drop=(), fresh=False, refresh=False, offline=False, log=None):
    """Add networks `new`, remove networks `drop` (exact entries) and regroup the blocks of one family.

    Owners already in the record are kept (also hand corrections) unless fresh is set. Networks without an owner
    are looked up (refresh: ask ip-api.com again instead of using the cache), unless offline is set: then they go
    to a block without owner, to be filled by a later run of enrich.py."""
    key = "ipv%d" % fam
    known = {} if fresh else block_info(rec, fam)
    dropped = {fmt(n) for n in drop}
    current = [n for n in nets(rec, fam) if fmt(n) not in dropped]
    networks = remove_subsumed(current + list(new))
    missing = [fmt(n) for n in networks if fmt(n) not in known or not known[fmt(n)]]
    found = {}
    if missing and not offline:
        addrs = {t: str(ipaddress.ip_network(t).network_address) for t in missing}
        res = lookup(sorted(set(addrs.values()), key=lambda a: ipaddress.ip_address(a).packed), refresh=refresh,
                     log=log)
        found = {t: res.get(a) or {} for t, a in addrs.items()}

    def info_for(n):
        t = fmt(n)
        return known.get(t) or found.get(t) or {}

    blocks = make_blocks(networks, info_for)
    if blocks:
        rec[key] = blocks
    else:
        rec.pop(key, None)
    return rec


# --- ip-api.com -----------------------------------------------------------------------------------------------

API = "http://ip-api.com/batch?fields=status,message,countryCode,isp,org,as,query"
_cache = None


def _cache_path():
    return os.path.join(CACHE, "ipapi.json")


def _load_cache():
    global _cache
    if _cache is None:
        try:
            with open(_cache_path(), encoding="utf-8") as f:
                _cache = json.load(f)
        except (OSError, ValueError):
            _cache = {}
    return _cache


def _save_cache():
    if _cache is None:
        return
    os.makedirs(CACHE, exist_ok=True)
    tmp = _cache_path() + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(_cache, f, ensure_ascii=False, sort_keys=True, indent=0)
    os.replace(tmp, _cache_path())


def _clean(text):
    return re.sub(r"\s+", " ", text or "").strip(" ,")


def _info(r):
    if r.get("status") != "success":
        return {"error": r.get("message") or "failed"}
    info = {"asn": (r.get("as") or "").split(" ", 1)[0], "isp": _clean(r.get("isp")), "org": _clean(r.get("org")),
            "country": r.get("countryCode") or ""}
    if not ASN.match(info["asn"]):
        info["asn"] = ""
    return {k: v for k, v in info.items() if v}


def lookup(addresses, refresh=False, log=None):
    """Owner of each address from the ip-api.com batch API (100 addresses per request, 15 requests a minute).

    Answers are kept in ~/.cache/scannersdb/ipapi.json, so a run that stops can be started again."""
    log = log or (lambda *a: print(*a, file=sys.stderr))
    cache = _load_cache()
    stamp = today()
    # refresh asks again for every address not already answered today, so a refresh that stops can be resumed
    todo = [a for a in dict.fromkeys(addresses)
            if a not in cache or (refresh and cache[a].get("checked") != stamp)]
    total = len(todo)
    for start in range(0, total, 100):
        chunk = todo[start:start + 100]
        for attempt in range(6):
            try:
                req = urllib.request.Request(API, data=json.dumps(chunk).encode(),
                                             headers={"Content-Type": "application/json", "User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as resp:
                    left = int(resp.headers.get("X-Rl", "1") or 1)
                    wait = int(resp.headers.get("X-Ttl", "60") or 60)
                    answer = json.load(resp)
                break
            except urllib.error.HTTPError as e:
                if e.code != 429 or attempt == 5:
                    raise
                time.sleep(61)
            except (OSError, ValueError):  # URLError, socket.timeout, reset connections, a cut-off answer
                if attempt == 5:
                    raise
                time.sleep(10 * (attempt + 1))
        for addr, r in zip(chunk, answer):
            info = _info(r)
            info["checked"] = stamp
            cache[addr] = info
        _save_cache()
        log("  ip-api: %d/%d" % (min(start + 100, total), total))
        if left <= 0 and start + 100 < total:
            time.sleep(wait + 1)
    return {a: {k: v for k, v in cache.get(a, {}).items() if k in INFO} for a in addresses}


# --- canonical format -----------------------------------------------------------------------------------------

def canonical(rec):
    """The record as it is written: keys in order, empty fields left out, lists sorted where order has no meaning."""
    out = {}
    for k in KEYS + sorted(set(rec) - set(KEYS) - {"id"}):
        v = rec.get(k)
        if v is None or v == "" or v == [] or v == {}:
            continue
        if k == "asn":
            v = _Flow(sorted(dict.fromkeys(v), key=lambda a: int(a[2:]) if ASN.match(a) else 1 << 40))
        elif k in ("ipv4", "ipv6"):
            v = [{bk: b[bk] for bk in BLOCK + sorted(set(b) - set(BLOCK)) if b.get(bk) not in (None, "", [])}
                 for b in v]
        out[k] = v
    return out


def dump(rec):
    body = yaml.dump(canonical(rec), Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=1 << 20,
                     default_flow_style=False)
    return HEAD + body


def save(rec):
    os.makedirs(DIR, exist_ok=True)
    text = dump(rec)
    tmp = path(rec["id"]) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path(rec["id"]))


# --- checks ---------------------------------------------------------------------------------------------------

def is_flag(text):
    return isinstance(text, str) and len(text) == 2 and all(0x1F1E6 <= ord(c) <= 0x1F1FF for c in text)


def check(rec):
    """Problems of one record, as text lines. An empty list means the record is fine."""
    p = []
    rid = rec.get("id", "?")
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", rid):
        p.append("file name: use lowercase letters, digits and dashes")
    for k in sorted(set(rec) - set(KEYS) - {"id"}):
        p.append("unknown field %r" % k)
    for k in REQUIRED:
        if not rec.get(k):
            p.append("missing %s" % k)
    for k in ("name", "legal_entity", "country", "note"):
        if k in rec and not isinstance(rec[k], str):
            p.append("%s: must be text" % k)
    if rec.get("status") and rec["status"] not in STATUSES:
        p.append("status: %r is not one of %s" % (rec["status"], ", ".join(STATUSES)))
    if rec.get("category") and rec["category"] not in CATEGORIES:
        p.append("category: %r is not one of %s" % (rec["category"], ", ".join(CATEGORIES)))
    if "flag" in rec and not is_flag(rec["flag"]):
        p.append("flag: must be a country flag emoji")
    if "flag" in rec and not rec.get("country"):
        p.append("flag without country")
    for k in ("website",):
        if k in rec and not (isinstance(rec[k], str) and URL.match(rec[k])):
            p.append("%s: must be an http(s) link" % k)
    if "opt_out" in rec and not (isinstance(rec["opt_out"], str) and (URL.match(rec["opt_out"])
                                                                     or EMAIL.match(rec["opt_out"]))):
        p.append("opt_out: must be an http(s) link or an e-mail address")
    for k in ("asn", "rdns", "user_agents", "sources"):
        if k in rec and not (isinstance(rec[k], list) and all(isinstance(x, str) and x for x in rec[k])):
            p.append("%s: must be a list of text" % k)
        elif k in rec and len(set(rec[k])) != len(rec[k]):
            p.append("%s: repeated entries" % k)
    for a in rec.get("asn") or []:
        if isinstance(a, str) and not ASN.match(a):
            p.append("asn: %r is not like AS12345" % a)
    for s in rec.get("sources") or []:
        if isinstance(s, str) and not URL.match(s):
            p.append("sources: %r is not an http(s) link" % s)
    if "updated" in rec and not (isinstance(rec["updated"], str) and DATE.match(rec["updated"])):
        p.append("updated: must be a quoted date 'YYYY-MM-DD'")
    if not rec.get("ipv4") and not rec.get("ipv6"):
        p.append("no networks: the record needs ipv4 or ipv6 blocks")
    for fam in (4, 6):
        p.extend(_check_family(rec, fam))
    return p


def _check_family(rec, fam):
    p = []
    key = "ipv%d" % fam
    blocks = rec.get(key)
    if blocks is None:
        return p
    if not isinstance(blocks, list) or not blocks:
        return ["%s: must be a list of blocks" % key]
    seen_keys = set()
    every = []
    for i, b in enumerate(blocks, 1):
        where = "%s block %d" % (key, i)
        if not isinstance(b, dict):
            p.append("%s: must be a mapping" % where)
            continue
        for k in sorted(set(b) - set(BLOCK)):
            p.append("%s: unknown field %r" % (where, k))
        if b.get("asn") and not (isinstance(b["asn"], str) and ASN.match(b["asn"])):
            p.append("%s: asn %r is not like AS12345" % (where, b["asn"]))
        if b.get("country") and not (isinstance(b["country"], str) and re.match(r"^[A-Z]{2}$", b["country"])):
            p.append("%s: country must be a two-letter code" % where)
        k = tuple(_norm(b.get(x, "")) if x in ("isp", "org") else b.get(x, "") for x in INFO)
        if k in seen_keys:
            p.append("%s: same owner as an earlier block, merge them" % where)
        seen_keys.add(k)
        ips = b.get("ip")
        if not isinstance(ips, list) or not ips:
            p.append("%s: ip must be a non-empty list" % where)
            continue
        parsed = []
        for text in ips:
            if not isinstance(text, str):
                p.append("%s: %r must be text (quote it)" % (where, text))
                continue
            try:
                n = ipaddress.ip_network(text)
            except ValueError:
                p.append("%s: %r is not a network (or has host bits set)" % (where, text))
                continue
            if fmt(n) != text:
                p.append("%s: write %r as %r" % (where, text, fmt(n)))
            if n.version != fam:
                p.append("%s: %s is IPv%d" % (where, text, n.version))
                continue
            if not n.is_global or n.is_multicast:
                p.append("%s: %s is not a public network" % (where, text))
            if n.prefixlen < WIDEST[fam]:
                p.append("%s: %s is wider than /%d" % (where, text, WIDEST[fam]))
            parsed.append(n)
        if parsed != sorted(parsed, key=sort_key):
            p.append("%s: networks are not sorted" % where)
        every.extend(parsed)
    if len(remove_subsumed(every)) != len(every):
        p.append("%s: repeated or overlapping networks" % key)
    elif [b for b in blocks if isinstance(b, dict)] != sorted([b for b in blocks if isinstance(b, dict)],
                                                               key=_block_key):
        p.append("%s: blocks are not sorted by ASN" % key)
    return p

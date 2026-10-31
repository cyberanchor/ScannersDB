# Scanner data

One YAML file per company or scanner: [`scanners/<id>.yaml`](scanners/). The tables in the main README and the ready
lists in [`lists/`](lists/) are built from these files by the scripts in [`tools/`](../tools/).

## Fields

Only `name`, `category`, `status`, `sources` and at least one network block are required; empty fields are left out.

| Field | Example | Meaning |
|---|---|---|
| `name` | `Censys` | Name of the scanner, project or company |
| `legal_entity` | `Censys, Inc.` | Company or institution that runs the scanners, as it names itself in its terms, imprint or registry entry. Left out when the operator does not say |
| `flag`, `country` | `🇺🇸`, `United States` | Country of the legal entity |
| `website` | `https://censys.com/` | Main site, or the page about the scans when there is no other |
| `category` | `search-engine` | Kind of operator, see [Categories](#categories) |
| `status` | `active` | `active`, or `inactive` for scanners that are gone (kept for reference, left out of the combined lists) |
| `asn` | `[AS398324, AS398705]` | Autonomous systems registered to the operator itself |
| `rdns` | `['*.censys-scanner.com']` | PTR (reverse DNS) names of the scanners, as shell patterns |
| `user_agents` | | HTTP User-Agent strings the scanners send |
| `opt_out` | link or e-mail | Where to ask to be left out of the scans |
| `note` | | What else is worth knowing: how the scanners identify themselves, data caveats |
| `ipv4`, `ipv6` | see below | Networks of the scanners, grouped by network owner |
| `sources` | | Where the networks and facts come from: upstream list files and the operator's own pages |
| `updated` | `'2026-10-31'` | Date of the last change |

### Network blocks

```yaml
ipv4:                         # from shodan.yaml
- asn: AS62
  isp: CyrusOne LLC
  org: Shodan LLC
  country: US
  ip:
  - '216.117.2.176/28'
- asn: AS174
  isp: Cogent Communications
  org: SHODAN, LLC
  country: US
  ip:
  - '207.90.244.0/24'
```

A block holds the networks of one owner. `asn`, `isp` and `org` are what [ip-api.com](https://ip-api.com/) reports for
the first address of each network: `isp` is the network that announces the range, `org` the organisation it is
assigned to, often the scanner itself. `country` is where the network is (two-letter code), not the scanner's home.
Single addresses are written without `/32` (`/128`), networks in CIDR form. Networks are sorted and quoted; adjacent
networks of one owner are merged, and names that differ only in punctuation count as one owner. Blocks are sorted by
ASN.

### Categories

| Category | Meaning |
|---|---|
| `search-engine` | Search engine for hosts and services (Shodan, Censys, FOFA ...) |
| `company` | Company scanning for its own products: attack surface, security ratings, threat intelligence, IP data |
| `research` | Research project, non-profit or measurement study |
| `university` | University or research institute |
| `government` | Government agency or national CERT |
| `hobby` | Private or hobby project (game server lists, personal scanners) |
| `unknown` | The operator does not say who it is |
| `cloud` | Whole cloud ranges, not only scanners. Left out of the combined lists |

## Lists

Built by `tools/export.py`; do not edit them by hand.

| File | Content |
|---|---|
| [`lists/scanners_v4.txt`](lists/scanners_v4.txt), [`lists/scanners_v6.txt`](lists/scanners_v6.txt) | Every active record except `cloud`, merged into the fewest networks. One network per line, no comments |
| [`lists/scanners.nft`](lists/scanners.nft) | The same as an nftables table `inet scannersdb` with two sets and an input chain that drops them |
| [`lists/scanners.ipset`](lists/scanners.ipset) | The same for `ipset restore` (sets `scannersdb_v4`, `scannersdb_v6`) |
| [`lists/cloud_v4.txt`](lists/cloud_v4.txt), [`lists/cloud_v6.txt`](lists/cloud_v6.txt) | The `cloud` records only: whole provider ranges, block them only if you know you get nothing from those clouds |
| [`lists/v4/<id>.txt`](lists/v4/), [`lists/v6/<id>.txt`](lists/v6/) | One list per record, inactive and cloud records included |
| [`lists/scanners.csv`](lists/scanners.csv) | One row per network: record, legal entity, category, status, network, ASN, ISP, ORG, network country |
| [`lists/scanners.json`](lists/scanners.json) | Every record with all fields and its counts |

## Sources

The networks are the union of these lists. Every record names the files it came from in `sources`.

<!-- sources:start -->
| Source                                                                                       | License                    | Read as     | Records |
|----------------------------------------------------------------------------------------------|----------------------------|-------------|--------:|
| [OpenFilters/internet-scanners](https://github.com/OpenFilters/internet-scanners)            | Unlicense (public domain)  | openfilters |     126 |
| [Connie-Wild/scanner-ip-list](https://github.com/Connie-Wild/scanner-ip-list)                | none stated                | lists       |      22 |
| [wdes/security](https://github.com/wdes/security)                                            | MPL-2.0                    | lists       |       4 |
| [security.wdes.eu](https://security.wdes.eu/)                                                | MPL-2.0                    | lists       |       3 |
| [cleverg0d/PublicGuard](https://github.com/cleverg0d/PublicGuard)                            | MIT (stated in the README) | sections    |      10 |
| [cleverg0d/PublicGuard pull request 1](https://github.com/cleverg0d/PublicGuard/pull/1)      | MIT (stated in the README) | sections    |      24 |
| [BinaryEdge API](https://api.binaryedge.io/v1/minions)                                       | —                          | json        |       1 |
| [LeakIX scanner list](https://scan.leakix.net/)                                              | —                          | json        |       1 |
| [ONYPHE IP ranges](https://www.onyphe.com/ip-ranges.txt)                                     | —                          | lists       |       1 |
| [Modat scanner ranges](https://scanner.modat.io/)                                            | —                          | lists       |       1 |
| [Tenable cloud scanner ranges](https://docs.tenable.com/ip-ranges/data.json)                 | —                          | json        |       1 |
| [Tenable Attack Surface Management ranges](https://docs.tenable.com/ip-ranges/asm/data.json) | —                          | json        |       1 |
<!-- sources:end -->

How they are read (`tools/sources.yaml`):

- **OpenFilters**: one `.nft` file per organisation, `inactive/` for scanners that are gone. `universities.nft` and
  `other.nft` hold many organisations with a comment line before each; they are split into one record per
  organisation.
- **Connie-Wild**: one `.txt` file per scanner. LeakIX is named in its README but has no file.
- **wdes/security**: the scanner files in `data/scanners/` (ANSSI, BinaryEdge API copy, Censys, internet-measurement.com)
  and the lists that its snow-scanner builds from PTR records and publishes on security.wdes.eu (Stretchoid,
  BinaryEdge, Shadowserver). Its collections (hand-picked bad IPs, Microsoft mail servers, AWS CloudFront) are not
  scanner lists and are not used; neither are the DigitalOcean helper files or `stretchoid_ranges.txt`, which holds
  whole Azure ranges.
- **PublicGuard**: `scanners_list.txt` with a comment line before each section, from `main` and from
  [pull request 1](https://github.com/cleverg0d/PublicGuard/pull/1).
- **Operator lists**: BinaryEdge API, LeakIX, ONYPHE, Modat and Tenable publish their own lists, read directly.

## Corrections

Some upstream entries are wrong: a range under the wrong company, a whole cloud network under a scanner, a prefix
that is not a valid network, a widened range. Each was checked against RDAP, ip-api.com and PTR records; the rules in
`tools/sources.yaml` leave them out or fix them on every import.

<!-- rules:start -->
| Record        | Network          | Source          | Action                                  | Why                                                                                                                                    |
|---------------|------------------|-----------------|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| mandiant      | 34.19.127.160/27 | openfilters     | written as 34.19.127.176/28             | written 34.19.127.176/27 upstream; the Mandiant page lists 34.19.127.176/28                                                            |
| alibaba-cloud | 47.234.0.0/15    | publicguard*    | written as 47.235.0.0/16, 47.236.0.0/16 | written 47.235.0.0/15, which is not a network; 47.234.0.0/16 belongs to Charter Communications, Alibaba Cloud LLC starts at 47.235.0.0 |
| tencent-cloud | 162.62.0.0/15    | publicguard*    | written as 162.62.0.0/16                | 162.63.0.0/16 belongs to UBS AG; only 162.62.0.0/16 is Tencent Cloud (Aceville Pte)                                                    |
| tencent-cloud | 45.197.79.0/24   | publicguard*    | left out                                | registered to Bedge Co (AS63139, Korea), not Tencent                                                                                   |
| tencent-cloud | 45.201.0.0/16    | publicguard*    | left out                                | registered to NZ Network Enterprise (AS147176, Thailand), not Tencent                                                                  |
| tencent-cloud | 156.240.62.0/24  | publicguard*    | left out                                | Cloud Innovation / Larus (AS17561), an address leasing company, not Tencent                                                            |
| detectify     | 103.203.57.0/24  | publicguard*    | left out                                | IPIP addresses (AS136180 Beijing Tiantexin), pasted twice into the Detectify section; they are in the IPIP record                      |
| zoomeye       | 103.224.80.0/20  | publicguard*    | left out                                | Hangzhou Jiweixia Network Technology (AS6134), not Knownsec                                                                            |
| zoomeye       | 45.249.244.0/22  | publicguard*    | left out                                | UCloud Information Technology (HK) (AS135377), a cloud range                                                                           |
| zoomeye       | 118.24.0.0/13    | publicguard*    | moved to tencent-cloud                  | Tencent Cloud (AS45090), a whole cloud range                                                                                           |
| fofa          | 103.224.212.0/22 | publicguard*    | left out                                | Trellian Pty (AS133618), a domain parking network                                                                                      |
| fofa          | 106.75.0.0/16    | publicguard*    | left out                                | Shanghai UCloud (AS9808), a whole cloud range                                                                                          |
| fofa          | 150.109.0.0/16   | publicguard*    | moved to tencent-cloud                  | Tencent Cloud (AS132203), a whole cloud range                                                                                          |
| binaryedge    | 185.162.235.0/24 | publicguard*    | left out                                | NorthernLightsCloud (AS213461); not in the BinaryEdge API list                                                                         |
| binaryedge    | 185.162.236.0/23 | publicguard*    | left out                                | AS209150 (Greece); not in the BinaryEdge API list                                                                                      |
| binaryedge    | 185.153.198.0/23 | publicguard*    | left out                                | IT Fruit (AS56380, Moldova); not in the BinaryEdge API list                                                                            |
| shadowserver  | 149.20.4.0/22    | publicguard*    | left out                                | Internet Systems Consortium (AS27321, AS30132, AS1280); no Shadowserver PTR                                                            |
| shadowserver  | 64.71.254.158    | publicguard*    | left out                                | Rogers Communications (AS812); no Shadowserver PTR                                                                                     |
| shadowserver  | 184.105.247.0/24 | publicguard-pr1 | left out                                | widened from 184.105.247.192/26; only that /26 has scan-*.shadowserver.io PTR records, the rest is other Hurricane Electric space      |
| shadowserver  | 65.49.20.0/24    | publicguard-pr1 | left out                                | widened from 65.49.20.64/26; only that /26 has scan-*.shadowserver.io PTR records                                                      |
| shadowserver  | 74.82.47.0/24    | publicguard-pr1 | left out                                | widened from 74.82.47.0/26; only that /26 has scan-*.shadowserver.io PTR records                                                       |
| rapid7        | 5.188.86.0/24    | publicguard*    | left out                                | Global Layer (AS49453), not Rapid7; no Rapid7 PTR records                                                                              |
| shodan        | 198.20.69.80     | publicguard*    | left out                                | PTR now names another host (chuck.nodeservers.net)                                                                                     |
| shodan        | 98.143.148.107   | publicguard*    | left out                                | PTR now names another host (1hjf.alisha.uk.com)                                                                                        |
| shodan        | 98.143.148.135   | publicguard*    | left out                                | PTR now names another host (api4.dizifrost.net)                                                                                        |
<!-- rules:end -->

## Adding or changing a scanner

- **New networks of a listed scanner**: add them to a block of the record (a new block with only an `ip:` list is fine)
  and run `tools/enrich.py <id>`, which looks up the owner and puts each network into the right block.
- **A new scanner**: copy a record of the same kind, keep the field order, add at least one source link, then run
  `tools/enrich.py <id>`.
- **Facts** (legal entity, PTR names, opt-out): edit the record and give the page that proves it in `sources`.

Then run `tools/export.py`, `tools/readme_table.py` and `tools/test_data.py`, and open a pull request with `data/` and
`README.md`. `test_data.py` stops on a broken record: unknown fields, a network that is not public or not canonical,
overlapping networks inside one record, unsorted blocks.

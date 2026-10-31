# Tools

Scripts that collect the scanner lists and keep the data files in sync. Python 3.9+ with PyYAML
(`dnf install python3-pyyaml` or `pip install pyyaml`); no other packages. Every script reads and writes the records
through `scdb.py`, so the files keep one format. `SCDB_DATA_DIR=/other/folder` points the scripts at a copy of the
records, `SCDB_CACHE` at another cache folder (default `~/.cache/scannersdb`).

| Script | What it does |
|---|---|
| `update.sh` | Full refresh: import, export, README tables, checks. Prints what changed; commit `data/` and `README.md` after reading it |
| `import_sources.py [--apply] [--offline] [--no-lookup] [--only SOURCES]` | Downloads every list in `sources.yaml`, applies the correction rules and compares with the records. With `--apply` it adds new networks (and new records). It never removes networks: those no upstream list has any more are listed in the report (`~/.cache/scannersdb/review.md`) for a decision by hand |
| `sources.yaml` | Upstream lists: download address, format, which record each file or section feeds, and the correction rules (networks put under the wrong company, invalid prefixes) |
| `enrich.py [--refresh] [ID ...]` | Looks up the owner (ASN, ISP, ORG, country) of networks that have none at ip-api.com and regroups the blocks. `--refresh` asks again for every network |
| `set_fields.py CHANGES.yaml` | Writes hand-checked fields into records (`{id: {field: value}}`, `null` removes a field, `rename: new-id` renames) |
| `export.py [OUTDIR]` | Builds `data/lists/`: combined lists, nftables table, ipset file, one list per record, CSV and JSON |
| `readme_table.py [--check]` | Writes the generated parts of `README.md` (counts, scanner tables) and `data/README.md` (sources, corrections) |
| `test_data.py [--fix]` | Checks every record, the overlaps between records, `sources.yaml`, `data/lists/` and the README tables. Run it before every commit; `--fix` rewrites records that are only off in format |
| `where.py ADDRESS ...` | Tells which record holds an address (also `-` to read addresses from stdin, for example from a firewall log) |
| `check_rdns.py [--limit N] [ID ...]` | Reverse DNS of single addresses against the record's `rdns` patterns. A PTR that names another host hints that a cloud address has been given to someone else. Only reports (`~/.cache/scannersdb/rdns.md`) |
| `scdb.py` | Shared module: load / save records in the canonical YAML format, checks, grouping networks by owner, the ip-api.com client and its cache |

## How a network gets into a record

1. `import_sources.py` reads every upstream list into (source, record, network). Lists name organisations in their own
   way: a file per organisation (OpenFilters, Connie-Wild, wdes), a comment line before each group (OpenFilters
   `universities.nft` and `other.nft`, PublicGuard) or one feed per operator. `sources.yaml` maps each of them to a
   record id.
2. The correction rules drop, move or rewrite the entries that were checked to be wrong.
3. Per record, networks inside a bigger network of the same record are dropped; the rest are looked up at ip-api.com
   (100 per request, 15 requests a minute, answers cached) and grouped into blocks by owner. Adjacent networks of one
   owner are merged.
4. The source files a record got networks from are added to its `sources`.

ip-api.com is free for non-commercial use and answers over plain HTTP; a first full run (about 35 000 networks) takes
about 25 minutes, later runs only look up new networks.

## Updating

```bash
tools/update.sh                # or step by step:
python3 tools/import_sources.py            # compare only, read ~/.cache/scannersdb/review.md
python3 tools/import_sources.py --apply    # add the new networks
python3 tools/export.py && python3 tools/readme_table.py && python3 tools/test_data.py
```

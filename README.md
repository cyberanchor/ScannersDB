<div align="center">

<img src="./assets/logo.png" width="200"></img>
<h1> ScannersDB </h1>

<sub>Database of internet-wide scanners: search engines, security companies, research projects and universities that scan the whole address space. One YAML file per company with its IPv4 blocks, legal entity, ASN, ISP and ORG.</sub>

<kbd>🛰️ Scanners</kbd> <kbd>🏢 Legal entity</kbd> <kbd>🖧 ASN / ISP / ORG</kbd> <kbd>🌍 Country</kbd> <kbd>🔎 PTR / User-Agent</kbd> <kbd>🚫 Opt-out</kbd>

</div>

> **Based on:** [internet-scanners](https://github.com/OpenFilters/internet-scanners) by [@OpenFilters](https://github.com/OpenFilters) | [scanner-ip-list](https://github.com/Connie-Wild/scanner-ip-list) by [@Connie-Wild](https://github.com/Connie-Wild) | [security](https://github.com/wdes/security) by [@wdes](https://github.com/wdes) ([security.wdes.eu](https://security.wdes.eu/)) | [PublicGuard](https://github.com/cleverg0d/PublicGuard) by [@cleverg0d](https://github.com/cleverg0d) (with [PR #1](https://github.com/cleverg0d/PublicGuard/pull/1)) | lists published by BinaryEdge, LeakIX, ONYPHE, Modat and Tenable

> **Data:** every scanner store in YAML [`data/scanners/`](./data/scanners/) ([fields](./data/README.md)), [scanners_v4.txt](./data/lists/scanners_v4.txt), [scanners_v6.txt](./data/lists/scanners_v6.txt), [scanners.csv](./data/lists/scanners.csv), [scanners.json](./data/lists/scanners.json)

## Scanners

Active scanners. `IPv4` is the number of networks in the record.

<!-- scanners:start -->
|   # | Company / resource                                  | Link                                                                          | Flag | Type          |  IPv4 | Record                                                                              |
|----:|-----------------------------------------------------|-------------------------------------------------------------------------------|------|---------------|------:|-------------------------------------------------------------------------------------|
|   1 | 360 Quake                                           | [quake.360.net](https://quake.360.net/)                                       | 🇨🇳   | search-engine |   640 | [360-quake](data/scanners/360-quake.yaml)                                           |
|   2 | A10 Networks                                        | [a10networks.com](https://www.a10networks.com/)                               | 🇺🇸   | company       |   654 | [a10networks](data/scanners/a10networks.yaml)                                       |
|   3 | "About this DNS measurement traffic"                | —                                                                             | ❓   | unknown       |     1 | [dns-measurement-notice](data/scanners/dns-measurement-notice.yaml)                 |
|   4 | Adscore                                             | [adscore.com](https://www.adscore.com/)                                       | 🇦🇪   | company       |    15 | [adscore](data/scanners/adscore.yaml)                                               |
|   5 | agentcensus                                         | [agentcensus.io](https://agentcensus.io/)                                     | ❓   | research      |     9 | [agentcensus](data/scanners/agentcensus.yaml)                                       |
|   6 | Alpha Strike Labs                                   | [alphastrike.io](https://www.alphastrike.io/)                                 | 🇩🇪   | company       |     5 | [alphastrike](data/scanners/alphastrike.yaml)                                       |
|   7 | ANSSI / CERT-FR                                     | [cyber.gouv.fr](https://cyber.gouv.fr/)                                       | 🇫🇷   | government    |     7 | [anssi](data/scanners/anssi.yaml)                                                   |
|   8 | Apcosys                                             | [apcosys.net](https://apcosys.net/)                                           | ❓   | research      |    34 | [apcosys](data/scanners/apcosys.yaml)                                               |
|   9 | b621.net hilbert-mapper                             | [b621.net](https://b621.net/)                                                 | ❓   | hobby         |     1 | [b621](data/scanners/b621.yaml)                                                     |
|  10 | BarkScan                                            | [barkscan.com](https://barkscan.com/)                                         | ❓   | search-engine |     1 | [barkscan](data/scanners/barkscan.yaml)                                             |
|  11 | benign.internet.survey.scan                         | —                                                                             | ❓   | unknown       |     1 | [internet-survey-scan](data/scanners/internet-survey-scan.yaml)                     |
|  12 | BinaryEdge                                          | [binaryedge.io](https://www.binaryedge.io/)                                   | 🇨🇭   | search-engine | 7,307 | [binaryedge](data/scanners/binaryedge.yaml)                                         |
|  13 | BitSight / Internet Census Group                    | [internet-census.org](https://www.internet-census.org/)                       | 🇺🇸   | company       |   171 | [bitsight](data/scanners/bitsight.yaml)                                             |
|  14 | bufferover.run                                      | [bufferover.run](https://bufferover.run/)                                     | ❓   | research      |    48 | [bufferover](data/scanners/bufferover.yaml)                                         |
|  15 | Cambridge Cybercrime Centre                         | [cambridgecybercrime.uk](https://www.cambridgecybercrime.uk/)                 | 🇬🇧   | university    |     1 | [cambridge](data/scanners/cambridge.yaml)                                           |
|  16 | Censys                                              | [censys.com](https://censys.com/)                                             | 🇺🇸   | search-engine |    16 | [censys](data/scanners/censys.yaml)                                                 |
|  17 | CERNET research scanner (202.112.47.x)              | —                                                                             | 🇨🇳   | research      |     2 | [cernet-research](data/scanners/cernet-research.yaml)                               |
|  18 | Criminal IP                                         | [criminalip.io](https://www.criminalip.io/)                                   | 🇰🇷   | search-engine |    64 | [criminalip](data/scanners/criminalip.yaml)                                         |
|  19 | CrowdStrike Falcon Surface                          | [crowdstrike.com](https://www.crowdstrike.com/)                               | 🇺🇸   | company       |     6 | [crowdstrike](data/scanners/crowdstrike.yaml)                                       |
|  20 | CyberCube                                           | [cybcube.com](https://www.cybcube.com/)                                       | 🇺🇸   | company       |     7 | [cybcube](data/scanners/cybcube.yaml)                                               |
|  21 | CyberGreen Institute                                | [cybergreen.net](https://cybergreen.net/)                                     | ❓   | research      |     1 | [cybergreen](data/scanners/cybergreen.yaml)                                         |
|  22 | CyberOK                                             | [cyberok.ru](https://www.cyberok.ru/)                                         | 🇷🇺   | company       |     1 | [cyberok](data/scanners/cyberok.yaml)                                               |
|  23 | CyberResilience (UpGuard)                           | [cyberresilience.io](https://cyberresilience.io/)                             | 🇺🇸   | company       |    58 | [cyberresilience](data/scanners/cyberresilience.yaml)                               |
|  24 | cyberscan.io                                        | [cyberscan.io](https://www.cyberscan.io/)                                     | 🇩🇪   | company       |     1 | [cyberscan](data/scanners/cyberscan.yaml)                                           |
|  25 | Cypex                                               | [cypex.ai](https://cypex.ai/)                                                 | ❓   | company       |    25 | [cypex](data/scanners/cypex.yaml)                                                   |
|  26 | Dataplane.org                                       | [dataplane.org](https://dataplane.org/)                                       | ❓   | research      |     2 | [dataplane](data/scanners/dataplane.yaml)                                           |
|  27 | Dataprovider.com                                    | [dataprovider.com](https://www.dataprovider.com/)                             | 🇳🇱   | search-engine |     1 | [dataprovider](data/scanners/dataprovider.yaml)                                     |
|  28 | Detectify                                           | [detectify.com](https://detectify.com/)                                       | 🇸🇪   | company       |    11 | [detectify](data/scanners/detectify.yaml)                                           |
|  29 | Driftnet (internet-measurement.com)                 | [driftnet.io](https://driftnet.io/)                                           | 🇬🇧   | search-engine |    34 | [driftnet](data/scanners/driftnet.yaml)                                             |
|  30 | Edgewatch                                           | [edgewatch.com](https://edgewatch.com/)                                       | 🇪🇸   | company       |     1 | [edgewatch](data/scanners/edgewatch.yaml)                                           |
|  31 | Entelijan                                           | [entelijan.com](https://entelijan.com/)                                       | ❓   | company       |     1 | [entelijan](data/scanners/entelijan.yaml)                                           |
|  32 | ESET Research                                       | [internet-scanner.eset.com](https://internet-scanner.eset.com/)               | 🇸🇰   | company       |     1 | [eset](data/scanners/eset.yaml)                                                     |
|  33 | Esslingen University                                | [hs-esslingen.de](https://www.hs-esslingen.de/)                               | 🇩🇪   | university    |     1 | [hs-esslingen](data/scanners/hs-esslingen.yaml)                                     |
|  34 | F6                                                  | [f6.ru](https://www.f6.ru/)                                                   | 🇷🇺   | company       |     6 | [f6](data/scanners/f6.yaml)                                                         |
|  35 | FH Münster                                          | [fh-muenster.de](https://www.fh-muenster.de/)                                 | 🇩🇪   | university    |     1 | [fh-muenster](data/scanners/fh-muenster.yaml)                                       |
|  36 | FlowIQ Labs                                         | [flowiq-labs.com](https://flowiq-labs.com/)                                   | ❓   | hobby         |    71 | [flowiq](data/scanners/flowiq.yaml)                                                 |
|  37 | FOFA                                                | [fofa.info](https://fofa.info/)                                               | 🇨🇳   | search-engine |   319 | [fofa](data/scanners/fofa.yaml)                                                     |
|  38 | Georgia Institute of Technology                     | [gatech.edu](https://www.gatech.edu/)                                         | 🇺🇸   | university    |     3 | [gatech](data/scanners/gatech.yaml)                                                 |
|  39 | "Global Network Asset Distribution Dashboard"       | —                                                                             | ❓   | unknown       |     1 | [global-network-asset-dashboard](data/scanners/global-network-asset-dashboard.yaml) |
|  40 | Group-IB                                            | [group-ib.com](https://www.group-ib.com/)                                     | 🇸🇬   | company       |    30 | [group-ib](data/scanners/group-ib.yaml)                                             |
|  41 | HackerTarget                                        | [hackertarget.com](https://hackertarget.com/)                                 | 🇦🇺   | company       |     3 | [hackertarget](data/scanners/hackertarget.yaml)                                     |
|  42 | Hadrian                                             | [hadrian.io](https://hadrian.io/)                                             | 🇳🇱   | company       |     7 | [hadrian](data/scanners/hadrian.yaml)                                               |
|  43 | Hasso Plattner Institute                            | [hpi.de](https://hpi.de/)                                                     | 🇩🇪   | university    |     1 | [hpi](data/scanners/hpi.yaml)                                                       |
|  44 | Hunter                                              | [hunter.how](https://hunter.how/)                                             | 🇨🇳   | search-engine | 3,525 | [hunter](data/scanners/hunter.yaml)                                                 |
|  45 | Infrawatch                                          | [infrawat.ch](https://infrawat.ch/)                                           | 🇬🇧   | search-engine |    32 | [infrawatch](data/scanners/infrawatch.yaml)                                         |
|  46 | Internet Measurement Research                       | [internetmeasurementresearch.com](https://internetmeasurementresearch.com/)   | 🇺🇸   | research      |     7 | [internetmeasurementresearch](data/scanners/internetmeasurementresearch.yaml)       |
|  47 | Internet Metrics                                    | [internet-metrics.com](https://internet-metrics.com/)                         | ❓   | research      |     2 | [internetmetrics](data/scanners/internetmetrics.yaml)                               |
|  48 | Internet Research Project                           | [internet-research-project.net](http://internet-research-project.net/)        | ❓   | research      |    11 | [internetresearchproject](data/scanners/internetresearchproject.yaml)               |
|  49 | Internet Scanning Project (internetresearch.center) | [internetresearch.center](https://internetresearch.center/)                   | ❓   | research      |    10 | [internetresearch-center](data/scanners/internetresearch-center.yaml)               |
|  50 | InterneTTL                                          | [internettl.org](http://www.internettl.org/)                                  | ❓   | research      |     1 | [internettl](data/scanners/internettl.yaml)                                         |
|  51 | Intrinsec                                           | [intrinsec.com](https://www.intrinsec.com/)                                   | 🇫🇷   | company       |     5 | [intrinsec](data/scanners/intrinsec.yaml)                                           |
|  52 | Intruder                                            | [intruder.io](https://www.intruder.io/)                                       | 🇬🇧   | company       |    36 | [intruder](data/scanners/intruder.yaml)                                             |
|  53 | IPGeolocation.io                                    | [ipgeolocation.io](https://ipgeolocation.io/)                                 | ❓   | company       |     1 | [ipgeolocation](data/scanners/ipgeolocation.yaml)                                   |
|  54 | IPinfo                                              | [ipinfo.io](https://ipinfo.io/)                                               | 🇺🇸   | company       | 2,263 | [ipinfo](data/scanners/ipinfo.yaml)                                                 |
|  55 | IPIP.NET                                            | [ipip.net](https://www.ipip.net/)                                             | 🇨🇳   | company       |   170 | [ipip](data/scanners/ipip.yaml)                                                     |
|  56 | IPTruth                                             | [iptruth.com](https://iptruth.com/)                                           | ❓   | unknown       |     8 | [iptruth](data/scanners/iptruth.yaml)                                               |
|  57 | "IPv6 Scan"                                         | —                                                                             | ❓   | unknown       |     0 | [ipv6-scan-notice](data/scanners/ipv6-scan-notice.yaml)                             |
|  58 | KI3                                                 | [ki3.org.cn](http://ki3.org.cn/)                                              | 🇨🇳   | research      |     8 | [ki3](data/scanners/ki3.yaml)                                                       |
|  59 | KittyScan                                           | —                                                                             | ❓   | hobby         |     3 | [kittyscan](data/scanners/kittyscan.yaml)                                           |
|  60 | Knoq                                                | [knoq.nl](https://knoq.nl/)                                                   | ❓   | research      |     1 | [knoq](data/scanners/knoq.yaml)                                                     |
|  61 | KU Leuven                                           | [kuleuven.be](https://www.kuleuven.be/)                                       | 🇧🇪   | university    |     2 | [kuleuven](data/scanners/kuleuven.yaml)                                             |
|  62 | Laburity                                            | [laburity.com](https://laburity.com/)                                         | ❓   | company       |     1 | [laburity](data/scanners/laburity.yaml)                                             |
|  63 | LeakIX                                              | [leakix.net](https://leakix.net/)                                             | ❓   | search-engine |    94 | [leakix](data/scanners/leakix.yaml)                                                 |
|  64 | Louisiana State University                          | [lsu.edu](https://www.lsu.edu/)                                               | 🇺🇸   | university    |     1 | [lsu](data/scanners/lsu.yaml)                                                       |
|  65 | Mandiant ASM (Google Threat Intelligence)           | [gtidocs.virustotal.com](https://gtidocs.virustotal.com/docs/asm-scan-ranges) | 🇺🇸   | company       |   106 | [mandiant](data/scanners/mandiant.yaml)                                             |
|  66 | matscan                                             | [github.com](https://github.com/mat-1/matscan)                                | ❓   | hobby         |     5 | [matscan](data/scanners/matscan.yaml)                                               |
|  67 | Max Planck Institute for Informatics                | [mpi-inf.mpg.de](https://www.mpi-inf.mpg.de/)                                 | 🇩🇪   | university    |    17 | [mpi-inf](data/scanners/mpi-inf.yaml)                                               |
|  68 | mcdb.app                                            | [mcdb.app](https://mcdb.app/)                                                 | ❓   | hobby         |     1 | [mcdb](data/scanners/mcdb.yaml)                                                     |
|  69 | Modat                                               | [modat.io](https://modat.io/)                                                 | 🇳🇱   | search-engine |    15 | [modat](data/scanners/modat.yaml)                                                   |
|  70 | Netlas                                              | [netlas.io](https://netlas.io/)                                               | 🇦🇲   | search-engine |    11 | [netlas](data/scanners/netlas.yaml)                                                 |
|  71 | NETSCOUT (internet-albedo.net)                      | [internet-albedo.net](https://www.internet-albedo.net/)                       | 🇺🇸   | company       |     1 | [netscout](data/scanners/netscout.yaml)                                             |
|  72 | Nokia Deepfield                                     | [nokia.com](https://www.nokia.com/genomecrawler/)                             | 🇫🇮   | company       |    16 | [nokia-deepfield](data/scanners/nokia-deepfield.yaml)                               |
|  73 | Normshield (tchelebi.io)                            | [blackkite.com](https://blackkite.com/)                                       | 🇺🇸   | company       |     2 | [normshield](data/scanners/normshield.yaml)                                         |
|  74 | NOTICE (NICT)                                       | [notice.go.jp](https://notice.go.jp/)                                         | 🇯🇵   | government    |    11 | [nict-notice](data/scanners/nict-notice.yaml)                                       |
|  75 | ODIN (Cyble)                                        | [getodin.com](https://getodin.com/)                                           | 🇺🇸   | search-engine |   471 | [cyble-odin](data/scanners/cyble-odin.yaml)                                         |
|  76 | ONLYSCANS                                           | [onlyscans.com](https://onlyscans.com/)                                       | 🇺🇸   | company       |     7 | [onlyscans](data/scanners/onlyscans.yaml)                                           |
|  77 | ONYPHE                                              | [onyphe.io](https://www.onyphe.io/)                                           | 🇫🇷   | search-engine |     9 | [onyphe](data/scanners/onyphe.yaml)                                                 |
|  78 | Open resolver scan (proper.com)                     | [proper.com](https://proper.com/)                                             | ❓   | research      |     1 | [proper](data/scanners/proper.yaml)                                                 |
|  79 | Paderborn University                                | [uni-paderborn.de](https://www.uni-paderborn.de/)                             | 🇩🇪   | university    |     2 | [paderborn](data/scanners/paderborn.yaml)                                           |
|  80 | Palo Alto Networks Cortex Xpanse                    | [paloaltonetworks.com](https://www.paloaltonetworks.com/cortex/cortex-xpanse) | 🇺🇸   | company       |    11 | [paloaltonetworks](data/scanners/paloaltonetworks.yaml)                             |
|  81 | ping-dash.com                                       | [ping-dash.com](https://ping-dash.com/)                                       | ❓   | unknown       |     1 | [ping-dash](data/scanners/ping-dash.yaml)                                           |
|  82 | pocnroll                                            | [pocnroll.com](https://pocnroll.com/)                                         | ❓   | research      |     1 | [pocnroll](data/scanners/pocnroll.yaml)                                             |
|  83 | Politecnico di Milano                               | [polimi.it](https://www.polimi.it/)                                           | 🇮🇹   | university    |     1 | [polimi](data/scanners/polimi.yaml)                                                 |
|  84 | ProbeTheNet                                         | [probethenet.com](https://probethenet.com/)                                   | ❓   | research      |     6 | [probethenet](data/scanners/probethenet.yaml)                                       |
|  85 | Qrator.Radar                                        | [radar.qrator.net](https://radar.qrator.net/)                                 | 🇨🇿   | company       |     1 | [qrator](data/scanners/qrator.yaml)                                                 |
|  86 | Rapid7 Project Sonar                                | [opendata.rapid7.com](https://opendata.rapid7.com/about/)                     | 🇺🇸   | company       |    11 | [rapid7](data/scanners/rapid7.yaml)                                                 |
|  87 | Recorded Future / SecurityTrails                    | [recordedfuture.com](https://www.recordedfuture.com/)                         | 🇺🇸   | company       |     7 | [recordedfuture](data/scanners/recordedfuture.yaml)                                 |
|  88 | Recyber                                             | [recyber.net](https://www.recyber.net/)                                       | ❓   | research      |    10 | [recyber](data/scanners/recyber.yaml)                                               |
|  89 | Research Scanner                                    | [research-scanner.com](https://research-scanner.com/)                         | ❓   | research      |    25 | [researchscanner](data/scanners/researchscanner.yaml)                               |
|  90 | Root Evidence                                       | [rootevidence.com](https://rootevidence.com/)                                 | 🇺🇸   | company       |   727 | [rootevidence](data/scanners/rootevidence.yaml)                                     |
|  91 | Ruhr University Bochum                              | [ruhr-uni-bochum.de](https://www.ruhr-uni-bochum.de/)                         | 🇩🇪   | university    |     7 | [rub](data/scanners/rub.yaml)                                                       |
|  92 | RWTH Aachen University                              | [rwth-aachen.de](https://www.rwth-aachen.de/)                                 | 🇩🇪   | university    |     1 | [rwth-aachen](data/scanners/rwth-aachen.yaml)                                       |
|  93 | scan.recover-entry.online                           | —                                                                             | ❓   | unknown       |     1 | [recover-entry](data/scanners/recover-entry.yaml)                                   |
|  94 | ScanSearch                                          | [scansearch.net](https://scansearch.net/)                                     | ❓   | search-engine |     2 | [scansearch](data/scanners/scansearch.yaml)                                         |
|  95 | "Security Research Traffic Notice"                  | —                                                                             | ❓   | unknown       |     1 | [security-research-notice](data/scanners/security-research-notice.yaml)             |
|  96 | securityresearch.net                                | —                                                                             | ❓   | unknown       |     1 | [securityresearch](data/scanners/securityresearch.yaml)                             |
|  97 | Shadowforce (Baffin Bay Networks)                   | [shadowforce.io](https://shadowforce.io/)                                     | 🇸🇪   | company       |    23 | [shadowforce](data/scanners/shadowforce.yaml)                                       |
|  98 | Shodan                                              | [shodan.io](https://www.shodan.io/)                                           | 🇺🇸   | search-engine |   100 | [shodan](data/scanners/shodan.yaml)                                                 |
|  99 | Stanford University                                 | [stanford.edu](https://www.stanford.edu/)                                     | 🇺🇸   | university    |     1 | [stanford](data/scanners/stanford.yaml)                                             |
| 100 | Stony Brook University                              | [stonybrook.edu](https://www.stonybrook.edu/)                                 | 🇺🇸   | university    |     1 | [stonybrook](data/scanners/stonybrook.yaml)                                         |
| 101 | Stretchoid                                          | [stretchoid.com](https://stretchoid.com/)                                     | ❓   | unknown       | 9,033 | [stretchoid](data/scanners/stretchoid.yaml)                                         |
| 102 | Synthient                                           | [synthient.com](https://synthient.com/)                                       | ❓   | company       |    22 | [synthient](data/scanners/synthient.yaml)                                           |
| 103 | Team Cymru                                          | [team-cymru.com](https://www.team-cymru.com/)                                 | 🇺🇸   | company       |     2 | [team-cymru](data/scanners/team-cymru.yaml)                                         |
| 104 | Technical University of Applied Sciences Augsburg   | [tha.de](https://www.tha.de/)                                                 | 🇩🇪   | university    |     1 | [th-augsburg](data/scanners/th-augsburg.yaml)                                       |
| 105 | Technical University of Denmark                     | [dtu.dk](https://www.dtu.dk/)                                                 | 🇩🇰   | university    |     1 | [dtu](data/scanners/dtu.yaml)                                                       |
| 106 | Technical University of Munich                      | [tum.de](https://www.tum.de/)                                                 | 🇩🇪   | university    |     3 | [tum](data/scanners/tum.yaml)                                                       |
| 107 | Tenable                                             | [tenable.com](https://www.tenable.com/)                                       | 🇺🇸   | company       |   101 | [tenable](data/scanners/tenable.yaml)                                               |
| 108 | The Shadowserver Foundation                         | [shadowserver.org](https://www.shadowserver.org/)                             | 🇺🇸   | research      |    21 | [shadowserver](data/scanners/shadowserver.yaml)                                     |
| 109 | Tsinghua University                                 | [tsinghua.edu.cn](https://www.tsinghua.edu.cn/)                               | 🇨🇳   | university    |     0 | [tsinghua](data/scanners/tsinghua.yaml)                                             |
| 110 | tttx                                                | [tttx.net](https://tttx.net/)                                                 | ❓   | research      |     9 | [tttx](data/scanners/tttx.yaml)                                                     |
| 111 | TU Dresden                                          | [tu-dresden.de](https://tu-dresden.de/)                                       | 🇩🇪   | university    |     9 | [tu-dresden](data/scanners/tu-dresden.yaml)                                         |
| 112 | University of California San Diego                  | [ucsd.edu](https://ucsd.edu/)                                                 | 🇺🇸   | university    |     1 | [ucsd](data/scanners/ucsd.yaml)                                                     |
| 113 | University of California, Santa Barbara             | [ucsb.edu](https://www.ucsb.edu/)                                             | 🇺🇸   | university    |     1 | [ucsb](data/scanners/ucsb.yaml)                                                     |
| 114 | University of Maryland                              | [umd.edu](https://umd.edu/)                                                   | 🇺🇸   | university    |     3 | [umd](data/scanners/umd.yaml)                                                       |
| 115 | University of Michigan                              | [umich.edu](https://umich.edu/)                                               | 🇺🇸   | university    |     3 | [umich](data/scanners/umich.yaml)                                                   |
| 116 | University of Twente                                | [utwente.nl](https://www.utwente.nl/)                                         | 🇳🇱   | university    |    38 | [utwente](data/scanners/utwente.yaml)                                               |
| 117 | University of Vienna                                | [univie.ac.at](https://www.univie.ac.at/)                                     | 🇦🇹   | university    |     3 | [univie](data/scanners/univie.yaml)                                                 |
| 118 | USC Information Sciences Institute                  | [isi.edu](https://www.isi.edu/)                                               | 🇺🇸   | university    |    13 | [usc-isi](data/scanners/usc-isi.yaml)                                               |
| 119 | Virginia Tech                                       | [vt.edu](https://www.vt.edu/)                                                 | 🇺🇸   | university    |     1 | [virginia-tech](data/scanners/virginia-tech.yaml)                                   |
| 120 | VirusTotal                                          | [virustotal.com](https://www.virustotal.com/)                                 | 🇺🇸   | company       |   111 | [virustotal](data/scanners/virustotal.yaml)                                         |
| 121 | VisionHeight                                        | [visionheight.com](https://visionheight.com/)                                 | 🇺🇸   | company       |   211 | [visionheight](data/scanners/visionheight.yaml)                                     |
| 122 | XMCO Serenety                                       | [xmco.fr](https://www.xmco.fr/)                                               | 🇫🇷   | company       |    44 | [xmco](data/scanners/xmco.yaml)                                                     |
| 123 | ZERN                                                | [zern.io](https://zern.io/)                                                   | ❓   | search-engine |   131 | [zern](data/scanners/zern.yaml)                                                     |
| 124 | ZoomEye                                             | [zoomeye.ai](https://www.zoomeye.ai/)                                         | 🇨🇳   | search-engine |    13 | [zoomeye](data/scanners/zoomeye.yaml)                                               |
<!-- scanners:end -->

## Inactive scanners

Gone or no longer reachable; kept for reference and left out of the combined lists.

<!-- inactive:start -->
|   # | Company / resource            | Link                                                                      | Flag | Type     | IPv4 | Record                                                                      |
|----:|-------------------------------|---------------------------------------------------------------------------|------|----------|-----:|-----------------------------------------------------------------------------|
|   1 | Academy for Internet Research | [academyforinternetresearch.org](https://academyforinternetresearch.org/) | ❓   | research |   66 | [academyforinternetresearch](data/scanners/academyforinternetresearch.yaml) |
|   2 | HSPO                          | [info-scan.hspo.io](https://info-scan.hspo.io/)                           | ❓   | unknown  |    5 | [hspo](data/scanners/hspo.yaml)                                             |
|   3 | netsecscan.net                | [netsecscan.net](http://www.netsecscan.net/)                              | ❓   | unknown  |   11 | [netsecscan](data/scanners/netsecscan.yaml)                                 |
|   4 | Open Port Statistics          | [openportstats.com](http://openportstats.com/)                            | ❓   | unknown  |  135 | [openportstats](data/scanners/openportstats.yaml)                           |
|   5 | ScanOpticon                   | [optout.scanopticon.com](https://optout.scanopticon.com/)                 | ❓   | unknown  |    3 | [scanopticon](data/scanners/scanopticon.yaml)                               |
|   6 | slowstack                     | [slowstack.tv](https://slowstack.tv/)                                     | ❓   | hobby    |    3 | [slowstack](data/scanners/slowstack.yaml)                                   |
<!-- inactive:end -->

## Cloud ranges

Whole cloud networks that PublicGuard lists as collectors. They hold ordinary customers too, so they are left out of the
combined lists; [`cloud_v4.txt`](./data/lists/cloud_v4.txt) has them separately.

<!-- cloud:start -->
|   # | Company / resource | Link                                              | Flag | Type  | IPv4 | Record                                            |
|----:|--------------------|---------------------------------------------------|------|-------|-----:|---------------------------------------------------|
|   1 | Alibaba Cloud      | [alibabacloud.com](https://www.alibabacloud.com/) | 🇨🇳   | cloud |   13 | [alibaba-cloud](data/scanners/alibaba-cloud.yaml) |
|   2 | Baidu              | [baidu.com](https://www.baidu.com/)               | 🇯🇵   | cloud |    1 | [baidu](data/scanners/baidu.yaml)                 |
|   3 | Tencent Cloud      | [tencentcloud.com](https://www.tencentcloud.com/) | 🇨🇳   | cloud |    5 | [tencent-cloud](data/scanners/tencent-cloud.yaml) |
<!-- cloud:end -->

## Quick start

**Lists**: [`scanners_v4.txt`](./data/lists/scanners_v4.txt) and [`scanners_v6.txt`](./data/lists/scanners_v6.txt) hold
every active scanner, one network per line; one scanner only: `data/lists/v4/<id>.txt`, for example
[`v4/shodan.txt`](./data/lists/v4/shodan.txt).

**Which scanner is this address?**

```bash
git clone https://github.com/cyberanchor/ScannersDB && cd ScannersDB
python3 tools/where.py 162.142.125.10
```

A record, shortened ([`data/scanners/censys.yaml`](./data/scanners/censys.yaml)):

```yaml
name: Censys
legal_entity: Censys, Inc.
flag: 🇺🇸
country: United States
website: https://censys.com/
category: search-engine
status: active
asn: [AS398324, AS398705, AS398722]
rdns:
- '*.censys-scanner.com'
user_agents:
- Mozilla/5.0 (compatible; CensysInspect/1.1; +https://about.censys.io/)
opt_out: https://docs.censys.com/docs/opt-out-of-data-collection
ipv4:
- asn: AS398324
  isp: Censys, Inc.
  org: Censys Inc
  country: US
  ip:
  - '66.132.148.0/24'
  - '66.132.153.0/24'
  - '162.142.125.0/24'      # ... 12 networks
- asn: AS398705
  isp: Censys, Inc.
  org: Censys, Inc.
  country: DE
  ip:
  - '167.94.146.0/24'
sources:
- https://github.com/OpenFilters/internet-scanners/blob/main/censys.nft
- https://github.com/Connie-Wild/scanner-ip-list/blob/main/censys.txt
- https://github.com/wdes/security/blob/main/data/scanners/censys.txt
- https://github.com/cleverg0d/PublicGuard/blob/main/scanners_list.txt
- https://github.com/cleverg0d/PublicGuard/pull/1
updated: '2026-10-31'
```

## Contributors

<a href="https://github.com/cyberanchor/ScannersDB/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=cyberanchor/ScannersDB" />
</a>

<!--
## Star History

<a href="https://www.star-history.com/#cyberanchor/ScannersDB&type=date&legend=bottom-right">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=cyberanchor/ScannersDB&type=date&theme=dark&legend=bottom-right" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=cyberanchor/ScannersDB&type=date&legend=bottom-right" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=cyberanchor/ScannersDB&type=date&legend=bottom-right" />
  </picture>
</a>
-->

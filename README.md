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
|   2 | A10 Networks                                        | [a10networks.com](https://www.a10networks.com/)                               | 🇺🇸   | company       |   661 | [a10networks](data/scanners/a10networks.yaml)                                       |
|   3 | "About this DNS measurement traffic"                | —                                                                             | ❓   | unknown       |     1 | [dns-measurement-notice](data/scanners/dns-measurement-notice.yaml)                 |
|   4 | Adscore                                             | [adscore.com](https://www.adscore.com/)                                       | 🇦🇪   | company       |    15 | [adscore](data/scanners/adscore.yaml)                                               |
|   5 | agentcensus                                         | [agentcensus.io](https://agentcensus.io/)                                     | ❓   | research      |     9 | [agentcensus](data/scanners/agentcensus.yaml)                                       |
|   6 | Akamai Connected Cloud (Linode) port scanner        | [linode.com](https://www.linode.com/)                                         | 🇺🇸   | company       |    39 | [linode-port-scanner](data/scanners/linode-port-scanner.yaml)                       |
|   7 | AllInsights                                         | [allinsights.one](https://allinsights.one/)                                   | ❓   | unknown       |    10 | [allinsights](data/scanners/allinsights.yaml)                                       |
|   8 | Alpha Strike Labs                                   | [alphastrike.io](https://www.alphastrike.io/)                                 | 🇩🇪   | company       |     5 | [alphastrike](data/scanners/alphastrike.yaml)                                       |
|   9 | ANSSI / CERT-FR                                     | [cyber.gouv.fr](https://cyber.gouv.fr/)                                       | 🇫🇷   | government    |     7 | [anssi](data/scanners/anssi.yaml)                                                   |
|  10 | Apcosys                                             | [apcosys.net](https://apcosys.net/)                                           | ❓   | research      |    34 | [apcosys](data/scanners/apcosys.yaml)                                               |
|  11 | b621.net hilbert-mapper                             | [b621.net](https://b621.net/)                                                 | ❓   | hobby         |     1 | [b621](data/scanners/b621.yaml)                                                     |
|  12 | BarkScan                                            | [barkscan.com](https://barkscan.com/)                                         | ❓   | search-engine |     1 | [barkscan](data/scanners/barkscan.yaml)                                             |
|  13 | benign.internet.survey.scan                         | —                                                                             | ❓   | unknown       |     1 | [internet-survey-scan](data/scanners/internet-survey-scan.yaml)                     |
|  14 | BinaryEdge                                          | [binaryedge.io](https://www.binaryedge.io/)                                   | 🇨🇭   | search-engine | 7,732 | [binaryedge](data/scanners/binaryedge.yaml)                                         |
|  15 | BitSight / Internet Census Group                    | [internet-census.org](https://www.internet-census.org/)                       | 🇺🇸   | company       |   171 | [bitsight](data/scanners/bitsight.yaml)                                             |
|  16 | bufferover.run                                      | [bufferover.run](https://bufferover.run/)                                     | ❓   | research      |    48 | [bufferover](data/scanners/bufferover.yaml)                                         |
|  17 | Cambridge Cybercrime Centre                         | [cambridgecybercrime.uk](https://www.cambridgecybercrime.uk/)                 | 🇬🇧   | university    |     1 | [cambridge](data/scanners/cambridge.yaml)                                           |
|  18 | CCN-CERT ELSA                                       | [ccn-cert.cni.es](https://www.ccn-cert.cni.es/)                               | 🇪🇸   | government    |   196 | [ccn-cert](data/scanners/ccn-cert.yaml)                                             |
|  19 | Censys                                              | [censys.com](https://censys.com/)                                             | 🇺🇸   | search-engine |    16 | [censys](data/scanners/censys.yaml)                                                 |
|  20 | CERNET research scanner (202.112.47.x)              | —                                                                             | 🇨🇳   | research      |     2 | [cernet-research](data/scanners/cernet-research.yaml)                               |
|  21 | Cert Spotter                                        | [sslmate.com](https://sslmate.com/certspotter/)                               | ❓   | company       |     7 | [certspotter](data/scanners/certspotter.yaml)                                       |
|  22 | Criminal IP                                         | [criminalip.io](https://www.criminalip.io/)                                   | 🇰🇷   | search-engine |    64 | [criminalip](data/scanners/criminalip.yaml)                                         |
|  23 | CrowdStrike Falcon Surface                          | [crowdstrike.com](https://www.crowdstrike.com/)                               | 🇺🇸   | company       |     6 | [crowdstrike](data/scanners/crowdstrike.yaml)                                       |
|  24 | CyberCube                                           | [cybcube.com](https://www.cybcube.com/)                                       | 🇺🇸   | company       |     7 | [cybcube](data/scanners/cybcube.yaml)                                               |
|  25 | CyberGreen Institute                                | [cybergreen.net](https://cybergreen.net/)                                     | ❓   | research      |     1 | [cybergreen](data/scanners/cybergreen.yaml)                                         |
|  26 | CyberOK                                             | [cyberok.ru](https://www.cyberok.ru/)                                         | 🇷🇺   | company       |     1 | [cyberok](data/scanners/cyberok.yaml)                                               |
|  27 | CyberResilience (UpGuard)                           | [cyberresilience.io](https://cyberresilience.io/)                             | 🇺🇸   | company       |    58 | [cyberresilience](data/scanners/cyberresilience.yaml)                               |
|  28 | cyberscan.io                                        | [cyberscan.io](https://www.cyberscan.io/)                                     | 🇩🇪   | company       |     1 | [cyberscan](data/scanners/cyberscan.yaml)                                           |
|  29 | Cypex                                               | [cypex.ai](https://cypex.ai/)                                                 | ❓   | company       |    25 | [cypex](data/scanners/cypex.yaml)                                                   |
|  30 | Dataplane.org                                       | [dataplane.org](https://dataplane.org/)                                       | ❓   | research      |     2 | [dataplane](data/scanners/dataplane.yaml)                                           |
|  31 | Dataprovider.com                                    | [dataprovider.com](https://www.dataprovider.com/)                             | 🇳🇱   | search-engine |     1 | [dataprovider](data/scanners/dataprovider.yaml)                                     |
|  32 | Detectify                                           | [detectify.com](https://detectify.com/)                                       | 🇸🇪   | company       |    11 | [detectify](data/scanners/detectify.yaml)                                           |
|  33 | Driftnet (internet-measurement.com)                 | [driftnet.io](https://driftnet.io/)                                           | 🇬🇧   | search-engine |    34 | [driftnet](data/scanners/driftnet.yaml)                                             |
|  34 | Edgewatch                                           | [edgewatch.com](https://edgewatch.com/)                                       | 🇪🇸   | company       |     1 | [edgewatch](data/scanners/edgewatch.yaml)                                           |
|  35 | Entelijan                                           | [entelijan.com](https://entelijan.com/)                                       | ❓   | company       |     1 | [entelijan](data/scanners/entelijan.yaml)                                           |
|  36 | ESET Research                                       | [internet-scanner.eset.com](https://internet-scanner.eset.com/)               | 🇸🇰   | company       |     1 | [eset](data/scanners/eset.yaml)                                                     |
|  37 | Esslingen University                                | [hs-esslingen.de](https://www.hs-esslingen.de/)                               | 🇩🇪   | university    |     1 | [hs-esslingen](data/scanners/hs-esslingen.yaml)                                     |
|  38 | F6                                                  | [f6.ru](https://www.f6.ru/)                                                   | 🇷🇺   | company       |     6 | [f6](data/scanners/f6.yaml)                                                         |
|  39 | FH Münster                                          | [fh-muenster.de](https://www.fh-muenster.de/)                                 | 🇩🇪   | university    |     1 | [fh-muenster](data/scanners/fh-muenster.yaml)                                       |
|  40 | FlowIQ Labs                                         | [flowiq-labs.com](https://flowiq-labs.com/)                                   | ❓   | hobby         |    71 | [flowiq](data/scanners/flowiq.yaml)                                                 |
|  41 | FOFA                                                | [fofa.info](https://fofa.info/)                                               | 🇨🇳   | search-engine |   319 | [fofa](data/scanners/fofa.yaml)                                                     |
|  42 | Georgia Institute of Technology                     | [gatech.edu](https://www.gatech.edu/)                                         | 🇺🇸   | university    |     3 | [gatech](data/scanners/gatech.yaml)                                                 |
|  43 | "Global Network Asset Distribution Dashboard"       | —                                                                             | ❓   | unknown       |     1 | [global-network-asset-dashboard](data/scanners/global-network-asset-dashboard.yaml) |
|  44 | Group-IB                                            | [group-ib.com](https://www.group-ib.com/)                                     | 🇸🇬   | company       |    30 | [group-ib](data/scanners/group-ib.yaml)                                             |
|  45 | HackerTarget                                        | [hackertarget.com](https://hackertarget.com/)                                 | 🇦🇺   | company       |     3 | [hackertarget](data/scanners/hackertarget.yaml)                                     |
|  46 | Hadrian                                             | [hadrian.io](https://hadrian.io/)                                             | 🇳🇱   | company       |     7 | [hadrian](data/scanners/hadrian.yaml)                                               |
|  47 | Hasso Plattner Institute                            | [hpi.de](https://hpi.de/)                                                     | 🇩🇪   | university    |     1 | [hpi](data/scanners/hpi.yaml)                                                       |
|  48 | HostedScan                                          | [hostedscan.com](https://hostedscan.com/)                                     | ❓   | company       |    73 | [hostedscan](data/scanners/hostedscan.yaml)                                         |
|  49 | Hunter                                              | [hunter.how](https://hunter.how/)                                             | 🇨🇳   | search-engine | 3,525 | [hunter](data/scanners/hunter.yaml)                                                 |
|  50 | Infrawatch                                          | [infrawat.ch](https://infrawat.ch/)                                           | 🇬🇧   | search-engine |    32 | [infrawatch](data/scanners/infrawatch.yaml)                                         |
|  51 | Internet Measurement Research                       | [internetmeasurementresearch.com](https://internetmeasurementresearch.com/)   | 🇺🇸   | research      |     7 | [internetmeasurementresearch](data/scanners/internetmeasurementresearch.yaml)       |
|  52 | Internet Metrics                                    | [internet-metrics.com](https://internet-metrics.com/)                         | ❓   | research      |     2 | [internetmetrics](data/scanners/internetmetrics.yaml)                               |
|  53 | Internet Research Project                           | [internet-research-project.net](http://internet-research-project.net/)        | ❓   | research      |    17 | [internetresearchproject](data/scanners/internetresearchproject.yaml)               |
|  54 | Internet Scanning Project (internetresearch.center) | [internetresearch.center](https://internetresearch.center/)                   | ❓   | research      |    10 | [internetresearch-center](data/scanners/internetresearch-center.yaml)               |
|  55 | InterneTTL                                          | [internettl.org](http://www.internettl.org/)                                  | ❓   | research      |     1 | [internettl](data/scanners/internettl.yaml)                                         |
|  56 | Intrinsec                                           | [intrinsec.com](https://www.intrinsec.com/)                                   | 🇫🇷   | company       |     5 | [intrinsec](data/scanners/intrinsec.yaml)                                           |
|  57 | Intruder                                            | [intruder.io](https://www.intruder.io/)                                       | 🇬🇧   | company       |    36 | [intruder](data/scanners/intruder.yaml)                                             |
|  58 | IPGeolocation.io                                    | [ipgeolocation.io](https://ipgeolocation.io/)                                 | ❓   | company       |     1 | [ipgeolocation](data/scanners/ipgeolocation.yaml)                                   |
|  59 | IPinfo                                              | [ipinfo.io](https://ipinfo.io/)                                               | 🇺🇸   | company       | 2,263 | [ipinfo](data/scanners/ipinfo.yaml)                                                 |
|  60 | IPIP.NET                                            | [ipip.net](https://www.ipip.net/)                                             | 🇨🇳   | company       |   170 | [ipip](data/scanners/ipip.yaml)                                                     |
|  61 | IPTruth                                             | [iptruth.com](https://iptruth.com/)                                           | ❓   | unknown       |     8 | [iptruth](data/scanners/iptruth.yaml)                                               |
|  62 | "IPv6 Scan"                                         | —                                                                             | ❓   | unknown       |     0 | [ipv6-scan-notice](data/scanners/ipv6-scan-notice.yaml)                             |
|  63 | KI3                                                 | [ki3.org.cn](http://ki3.org.cn/)                                              | 🇨🇳   | research      |     8 | [ki3](data/scanners/ki3.yaml)                                                       |
|  64 | KittyScan                                           | —                                                                             | ❓   | hobby         |     3 | [kittyscan](data/scanners/kittyscan.yaml)                                           |
|  65 | Knoq                                                | [knoq.nl](https://knoq.nl/)                                                   | ❓   | research      |     1 | [knoq](data/scanners/knoq.yaml)                                                     |
|  66 | KU Leuven                                           | [kuleuven.be](https://www.kuleuven.be/)                                       | 🇧🇪   | university    |     2 | [kuleuven](data/scanners/kuleuven.yaml)                                             |
|  67 | Laburity                                            | [laburity.com](https://laburity.com/)                                         | ❓   | company       |     1 | [laburity](data/scanners/laburity.yaml)                                             |
|  68 | LeakIX                                              | [leakix.net](https://leakix.net/)                                             | ❓   | search-engine |    94 | [leakix](data/scanners/leakix.yaml)                                                 |
|  69 | Louisiana State University                          | [lsu.edu](https://www.lsu.edu/)                                               | 🇺🇸   | university    |     1 | [lsu](data/scanners/lsu.yaml)                                                       |
|  70 | Mandiant ASM (Google Threat Intelligence)           | [gtidocs.virustotal.com](https://gtidocs.virustotal.com/docs/asm-scan-ranges) | 🇺🇸   | company       |   106 | [mandiant](data/scanners/mandiant.yaml)                                             |
|  71 | matscan                                             | [github.com](https://github.com/mat-1/matscan)                                | ❓   | hobby         |     5 | [matscan](data/scanners/matscan.yaml)                                               |
|  72 | Max Planck Institute for Informatics                | [mpi-inf.mpg.de](https://www.mpi-inf.mpg.de/)                                 | 🇩🇪   | university    |    17 | [mpi-inf](data/scanners/mpi-inf.yaml)                                               |
|  73 | mcdb.app                                            | [mcdb.app](https://mcdb.app/)                                                 | ❓   | hobby         |     1 | [mcdb](data/scanners/mcdb.yaml)                                                     |
|  74 | Modat                                               | [modat.io](https://modat.io/)                                                 | 🇳🇱   | search-engine |    15 | [modat](data/scanners/modat.yaml)                                                   |
|  75 | Netlas                                              | [netlas.io](https://netlas.io/)                                               | 🇦🇲   | search-engine |    11 | [netlas](data/scanners/netlas.yaml)                                                 |
|  76 | NETSCOUT (internet-albedo.net)                      | [internet-albedo.net](https://www.internet-albedo.net/)                       | 🇺🇸   | company       |     1 | [netscout](data/scanners/netscout.yaml)                                             |
|  77 | Nokia Deepfield                                     | [nokia.com](https://www.nokia.com/genomecrawler/)                             | 🇫🇮   | company       |    16 | [nokia-deepfield](data/scanners/nokia-deepfield.yaml)                               |
|  78 | Normshield (tchelebi.io)                            | [blackkite.com](https://blackkite.com/)                                       | 🇺🇸   | company       |     2 | [normshield](data/scanners/normshield.yaml)                                         |
|  79 | NOTICE (NICT)                                       | [notice.go.jp](https://notice.go.jp/)                                         | 🇯🇵   | government    |    11 | [nict-notice](data/scanners/nict-notice.yaml)                                       |
|  80 | ODIN (Cyble)                                        | [getodin.com](https://getodin.com/)                                           | 🇺🇸   | search-engine |   471 | [cyble-odin](data/scanners/cyble-odin.yaml)                                         |
|  81 | ONLYSCANS                                           | [onlyscans.com](https://onlyscans.com/)                                       | 🇺🇸   | company       |     7 | [onlyscans](data/scanners/onlyscans.yaml)                                           |
|  82 | ONYPHE                                              | [onyphe.io](https://www.onyphe.io/)                                           | 🇫🇷   | search-engine |     9 | [onyphe](data/scanners/onyphe.yaml)                                                 |
|  83 | Open resolver scan (proper.com)                     | [proper.com](https://proper.com/)                                             | ❓   | research      |     1 | [proper](data/scanners/proper.yaml)                                                 |
|  84 | Paderborn University                                | [uni-paderborn.de](https://www.uni-paderborn.de/)                             | 🇩🇪   | university    |     2 | [paderborn](data/scanners/paderborn.yaml)                                           |
|  85 | Palo Alto Networks Cortex Xpanse                    | [paloaltonetworks.com](https://www.paloaltonetworks.com/cortex/cortex-xpanse) | 🇺🇸   | company       |    11 | [paloaltonetworks](data/scanners/paloaltonetworks.yaml)                             |
|  86 | ping-dash.com                                       | [ping-dash.com](https://ping-dash.com/)                                       | ❓   | unknown       |     1 | [ping-dash](data/scanners/ping-dash.yaml)                                           |
|  87 | pocnroll                                            | [pocnroll.com](https://pocnroll.com/)                                         | ❓   | research      |     1 | [pocnroll](data/scanners/pocnroll.yaml)                                             |
|  88 | Politecnico di Milano                               | [polimi.it](https://www.polimi.it/)                                           | 🇮🇹   | university    |     1 | [polimi](data/scanners/polimi.yaml)                                                 |
|  89 | portscan.work                                       | [portscan.work](https://portscan.work/)                                       | ❓   | unknown       |     4 | [portscan-work](data/scanners/portscan-work.yaml)                                   |
|  90 | ProbeTheNet                                         | [probethenet.com](https://probethenet.com/)                                   | ❓   | research      |     6 | [probethenet](data/scanners/probethenet.yaml)                                       |
|  91 | Qrator.Radar                                        | [radar.qrator.net](https://radar.qrator.net/)                                 | 🇨🇿   | company       |     1 | [qrator](data/scanners/qrator.yaml)                                                 |
|  92 | Rapid7 Project Sonar                                | [opendata.rapid7.com](https://opendata.rapid7.com/about/)                     | 🇺🇸   | company       |    11 | [rapid7](data/scanners/rapid7.yaml)                                                 |
|  93 | Recorded Future / SecurityTrails                    | [recordedfuture.com](https://www.recordedfuture.com/)                         | 🇺🇸   | company       |     7 | [recordedfuture](data/scanners/recordedfuture.yaml)                                 |
|  94 | Recyber                                             | [recyber.net](https://www.recyber.net/)                                       | ❓   | research      |    10 | [recyber](data/scanners/recyber.yaml)                                               |
|  95 | Research Scanner                                    | [research-scanner.com](https://research-scanner.com/)                         | ❓   | research      |    25 | [researchscanner](data/scanners/researchscanner.yaml)                               |
|  96 | Root Evidence                                       | [rootevidence.com](https://rootevidence.com/)                                 | 🇺🇸   | company       |   727 | [rootevidence](data/scanners/rootevidence.yaml)                                     |
|  97 | Ruhr University Bochum                              | [ruhr-uni-bochum.de](https://www.ruhr-uni-bochum.de/)                         | 🇩🇪   | university    |     7 | [rub](data/scanners/rub.yaml)                                                       |
|  98 | RWTH Aachen University                              | [rwth-aachen.de](https://www.rwth-aachen.de/)                                 | 🇩🇪   | university    |     1 | [rwth-aachen](data/scanners/rwth-aachen.yaml)                                       |
|  99 | SAINT                                               | [carson-saint.com](https://www.carson-saint.com/)                             | 🇺🇸   | company       |     4 | [saint](data/scanners/saint.yaml)                                                   |
| 100 | scan.recover-entry.online                           | —                                                                             | ❓   | unknown       |     1 | [recover-entry](data/scanners/recover-entry.yaml)                                   |
| 101 | ScanSearch                                          | [scansearch.net](https://scansearch.net/)                                     | ❓   | search-engine |     2 | [scansearch](data/scanners/scansearch.yaml)                                         |
| 102 | "Security Research Traffic Notice"                  | —                                                                             | ❓   | unknown       |     1 | [security-research-notice](data/scanners/security-research-notice.yaml)             |
| 103 | securityresearch.net                                | —                                                                             | ❓   | unknown       |     1 | [securityresearch](data/scanners/securityresearch.yaml)                             |
| 104 | Shadowforce (Baffin Bay Networks)                   | [shadowforce.io](https://shadowforce.io/)                                     | 🇸🇪   | company       |    23 | [shadowforce](data/scanners/shadowforce.yaml)                                       |
| 105 | Shodan                                              | [shodan.io](https://www.shodan.io/)                                           | 🇺🇸   | search-engine |   100 | [shodan](data/scanners/shodan.yaml)                                                 |
| 106 | SOCRadar                                            | [socradar.io](https://socradar.io/)                                           | ❓   | company       |    20 | [socradar](data/scanners/socradar.yaml)                                             |
| 107 | Sonic (offnet-scand)                                | [sonic.com](https://www.sonic.com/)                                           | 🇺🇸   | company       |     2 | [sonic](data/scanners/sonic.yaml)                                                   |
| 108 | Stanford University                                 | [stanford.edu](https://www.stanford.edu/)                                     | 🇺🇸   | university    |     1 | [stanford](data/scanners/stanford.yaml)                                             |
| 109 | Stony Brook University                              | [stonybrook.edu](https://www.stonybrook.edu/)                                 | 🇺🇸   | university    |     1 | [stonybrook](data/scanners/stonybrook.yaml)                                         |
| 110 | Stretchoid                                          | [stretchoid.com](https://stretchoid.com/)                                     | ❓   | unknown       | 9,033 | [stretchoid](data/scanners/stretchoid.yaml)                                         |
| 111 | Synthient                                           | [synthient.com](https://synthient.com/)                                       | ❓   | company       |    22 | [synthient](data/scanners/synthient.yaml)                                           |
| 112 | Team Cymru                                          | [team-cymru.com](https://www.team-cymru.com/)                                 | 🇺🇸   | company       |     2 | [team-cymru](data/scanners/team-cymru.yaml)                                         |
| 113 | Technical University of Applied Sciences Augsburg   | [tha.de](https://www.tha.de/)                                                 | 🇩🇪   | university    |     1 | [th-augsburg](data/scanners/th-augsburg.yaml)                                       |
| 114 | Technical University of Denmark                     | [dtu.dk](https://www.dtu.dk/)                                                 | 🇩🇰   | university    |     1 | [dtu](data/scanners/dtu.yaml)                                                       |
| 115 | Technical University of Munich                      | [tum.de](https://www.tum.de/)                                                 | 🇩🇪   | university    |     3 | [tum](data/scanners/tum.yaml)                                                       |
| 116 | Tenable                                             | [tenable.com](https://www.tenable.com/)                                       | 🇺🇸   | company       |   101 | [tenable](data/scanners/tenable.yaml)                                               |
| 117 | The Shadowserver Foundation                         | [shadowserver.org](https://www.shadowserver.org/)                             | 🇺🇸   | research      |    21 | [shadowserver](data/scanners/shadowserver.yaml)                                     |
| 118 | Tsinghua University                                 | [tsinghua.edu.cn](https://www.tsinghua.edu.cn/)                               | 🇨🇳   | university    |     0 | [tsinghua](data/scanners/tsinghua.yaml)                                             |
| 119 | tttx                                                | [tttx.net](https://tttx.net/)                                                 | ❓   | research      |     9 | [tttx](data/scanners/tttx.yaml)                                                     |
| 120 | TU Dresden                                          | [tu-dresden.de](https://tu-dresden.de/)                                       | 🇩🇪   | university    |     9 | [tu-dresden](data/scanners/tu-dresden.yaml)                                         |
| 121 | University of California San Diego                  | [ucsd.edu](https://ucsd.edu/)                                                 | 🇺🇸   | university    |     1 | [ucsd](data/scanners/ucsd.yaml)                                                     |
| 122 | University of California, Santa Barbara             | [ucsb.edu](https://www.ucsb.edu/)                                             | 🇺🇸   | university    |     1 | [ucsb](data/scanners/ucsb.yaml)                                                     |
| 123 | University of Maryland                              | [umd.edu](https://umd.edu/)                                                   | 🇺🇸   | university    |     3 | [umd](data/scanners/umd.yaml)                                                       |
| 124 | University of Michigan                              | [umich.edu](https://umich.edu/)                                               | 🇺🇸   | university    |     3 | [umich](data/scanners/umich.yaml)                                                   |
| 125 | University of Twente                                | [utwente.nl](https://www.utwente.nl/)                                         | 🇳🇱   | university    |    38 | [utwente](data/scanners/utwente.yaml)                                               |
| 126 | University of Vienna                                | [univie.ac.at](https://www.univie.ac.at/)                                     | 🇦🇹   | university    |     3 | [univie](data/scanners/univie.yaml)                                                 |
| 127 | USC Information Sciences Institute                  | [isi.edu](https://www.isi.edu/)                                               | 🇺🇸   | university    |    13 | [usc-isi](data/scanners/usc-isi.yaml)                                               |
| 128 | Virginia Tech                                       | [vt.edu](https://www.vt.edu/)                                                 | 🇺🇸   | university    |     1 | [virginia-tech](data/scanners/virginia-tech.yaml)                                   |
| 129 | VirusTotal                                          | [virustotal.com](https://www.virustotal.com/)                                 | 🇺🇸   | company       |   111 | [virustotal](data/scanners/virustotal.yaml)                                         |
| 130 | VisionHeight                                        | [visionheight.com](https://visionheight.com/)                                 | 🇺🇸   | company       |   211 | [visionheight](data/scanners/visionheight.yaml)                                     |
| 131 | XMCO Serenety                                       | [xmco.fr](https://www.xmco.fr/)                                               | 🇫🇷   | company       |    44 | [xmco](data/scanners/xmco.yaml)                                                     |
| 132 | ZERN                                                | [zern.io](https://zern.io/)                                                   | ❓   | search-engine |   131 | [zern](data/scanners/zern.yaml)                                                     |
| 133 | ZoomEye                                             | [zoomeye.ai](https://www.zoomeye.ai/)                                         | 🇨🇳   | search-engine |    13 | [zoomeye](data/scanners/zoomeye.yaml)                                               |
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

## Donate

Support this project with Monero (XMR):

```
4BEb8AUfSwQbGaHSVnBn2sMkFsYvrA6Eq4UyEf3JtcEZJd9eSm96YiZZwMWunKq6fUZSuAomwY4P835ybppBxi3NRY2ncMY
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

# V10 release manifest

Created: 2 October 2026

Repository revision: `7434615b5b8538c978b8608fab9c11e0e31f0344`

Environment: Python 3.12.14 on Microsoft Windows 10.0.26200

The `raw` directory is intentionally ignored by Git. It is the local preservation copy
for later attachment to a public data release. The interrupted study 01 must be treated
as a three-file SQLite WAL set. None of these files may be edited in place.

| File | Class | Bytes | SHA-256 | Origin |
|---|---|---:|---|---|
| `raw/nvidia-nim-v10-gpt-oss-reliability-01.sqlite` | Raw | 4,096 | `0AB48B25CBA617ED3A4ACCA0161813B314C095EF63544BB4AF60769EB1012977` | Preserved study 01 main database |
| `raw/nvidia-nim-v10-gpt-oss-reliability-01.sqlite-shm` | Raw | 32,768 | `BB40F7475A83344430147C4D95C2E73AA560E4316AB977011E89AB5E5CE89B8B` | Preserved study 01 shared-memory sidecar |
| `raw/nvidia-nim-v10-gpt-oss-reliability-01.sqlite-wal` | Raw | 1,095,952 | `0F59468435144C9A3B03A02970F54DD651D7CE50250AF27B5AB4348E5D1370B5` | Preserved study 01 write-ahead log containing the interrupted record |
| `raw/nvidia-nim-v10-gpt-oss-reliability-02.sqlite` | Raw | 16,965,632 | `A5177BED157BCCBC3B9567F16269EC0EB2E2CACF93078777E84A8C70D7434331` | Completed replacement cohort |
| `derived/frozen-analysis.json` | Derived | 26,110 | `AAA4D8FCF199E476783EDFD8A9DEB132C31005896DA74576B93DADDA4E8F9BAC` | Analyzer frozen at study launch |
| `derived/hardened-analysis.json` | Derived | 31,793 | `EA4021F8265D86DE05F3864367727BEAF84535DCFC3C05C979B1FC96FFB08B89` | Post-freeze integrity analyzer at revision `7434615` |

The two analyzers agree on every shared estimate and all 11 frozen progression rules.
The hardened output adds execution-structure, provider-alignment, raw-metric
recomputation and family-level reporting checks. These additions do not change a frozen
threshold.

Before public upload, the credential scan, trial-level export, provider-identifier
policy check and independent human manifest check in
`docs/v10-data-release-checklist.md` must still be completed.

# Dataset Assessment: Public Clinical Dataset Worked Example

## Decision

MIMIC-IV Clinical Database Demo v2.2 is the selected initial worked example.
It is a 100-patient, open-access, ODbL-licensed PhysioNet dataset with
relational hospital and ICU CSV tables. It supports realistic admitted-episode
staging and local-file diagnostics, but it is not authoritative Australian
AR-DRG evidence and is not authoritative ICD-10-AM, ACHI, ACS, or NWAU
evidence by itself.

The default tutorial must therefore fail closed until either:

- Australian AR-DRG provenance is supplied from a local licensed/precomputed
  source, or
- an explicitly synthetic Australian AR-DRG overlay fixture is selected for
  runnable documentation only.

## Candidate Inventory

| Dataset | Access and License | Size | Fields | Fit | Decision |
| --- | --- | ---: | --- | --- | --- |
| MIMIC-IV Clinical Database Demo v2.2 | Open-access PhysioNet files under Open Data Commons Open Database License v1.0. Citation DOI: `10.13026/dp1f-ex47`. | 15.5 MB uncompressed; 15.4 MB ZIP. | `admissions`, `patients`, `diagnoses_icd`, `procedures_icd`, `drgcodes`, `transfers`, ICU stay tables. | Best initial fit for admitted-episode staging and local-file workflow. | Selected initial worked example. |
| MIMIC-IV-ED Demo v2.2 | Open-access PhysioNet files under Open Data Commons Open Database License v1.0. Citation DOI: `10.13026/jzz5-vs76`. | 111.8 KB uncompressed; 95.5 KB ZIP. | `edstays`, `diagnosis`, `medrecon`, `pyxis`, `triage`, `vitalsign`. | Good future ED example, but ED classification support is separate from acute admitted workflow. | Defer to separate ED track/issue. |
| MIMIC-IV Demo in MEDS v0.0.1 | Open-access PhysioNet files under Open Data Commons Open Database License v1.0. Citation DOI: `10.13026/t2y8-ea41`. | 5.7 MB uncompressed; 4.7 MB ZIP. | MEDS event stream, code metadata, split metadata. | Useful for event-stream interoperability, not first acute CSV tutorial. | Defer to interop track/issue. |
| MIMIC-IV Clinical Database Demo on FHIR v2.1.0 | Open-access PhysioNet files under Open Data Commons Open Database License v1.0. Citation DOI: `10.13026/vphg-y548`. | 49.5 MB uncompressed; 49.5 MB ZIP. | FHIR `Patient`, `Encounter`, `Condition`, `Procedure`, `Observation`, and related resources. | Useful for FHIR/API boundary documentation, but requires a different parser and data model. | Defer to FHIR/MEDS interop track/issue. |
| Synthea synthetic patient records | Apache-2.0 generator and downloadable synthetic datasets. | Varies by generated cohort. | FHIR, C-CDA, CSV, CPCDS-style synthetic records. | Strong comparison point for no-real-data fixtures; less useful for real-data provenance. | Keep as synthetic comparison/future example. |

## Access and Local Cache Rules

- Raw public clinical dataset files stay out of git, even when the upstream
  license permits access.
- Local cache paths are user supplied and may point to downloaded PhysioNet
  directories, but committed files are limited to manifests, metadata, tiny
  synthetic fixtures, and documentation.
- Any real public-data-derived output is local-only unless a disclosure-risk
  review classifies it as commit-safe.
- Tiny fixtures committed for tests must be synthetic and MIMIC-shaped, not raw
  rows copied from MIMIC.

## Australian Classification Boundary

MIMIC US DRGs, ICD-9-CM, ICD-10-CM, and ICD-10-PCS fields are not authoritative
Australian AR-DRG, ICD-10-AM, ACHI, or ACS inputs. The worked example can show
how to stage episodes and where classification provenance is required. It must
not claim Australian NWAU output from MIMIC alone.

In short: MIMIC is not authoritative Australian AR-DRG evidence.

## Follow-Up Issues

- `#346`: MIMIC-IV-ED public dataset worked example.
- `#347`: FHIR and MEDS public dataset interop worked examples.
- `#348`: Public dataset suitability registry.
- `#349`: Public dataset downloader and cache guard.
- `#350`: Reusable public dataset provenance and data-quality report contract.
- `#351`: Worked-example surface conformance harness.
- `#352`: Public dataset disclosure-risk and safe-output policy.
- `#353`: Worked-example scenario and sensitivity report.
- `#354`: Branch workflow-file issue found during pushed Conductor evidence.

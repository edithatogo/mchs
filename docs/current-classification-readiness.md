# Current classification readiness

Issue #399, parent #396; related #204, #205, #206. Existing provider and local-asset
contracts remain the integration interfaces. No licensed grouper is implemented
by the new raw-input inventory helper.

The [IHACPA EPD13 guide, sections 2.2–2.3](https://www.ihacpa.gov.au/sites/default/files/2025-05/epd_short_listicd-10-am_thirteenth_edition_user-guide.pdf)
identifies SNOMED CT-AU EDRS → ICD-10-AM → EPD Short List as the Australian
mapping route. These maps require appropriate access/licensing; the public EPD
Short List → ECDG spreadsheet alone does not resolve SNOMED. US ICD-10-CM,
WHO ICD-10 and Australian ICD-10-AM are not interchangeable maps.

A diagnosis group is not a full AECC class. The
[AECC definitions manual](https://www.ihacpa.gov.au/sites/default/files/2022-08/aecc_definitions_manual_version_4_0.pdf)
requires age, end status, triage and arrival transport for complexity and clinical
care commencement for relevant episode branching. Referral source is not arrival
transport; departure time is not end status. The helper returns missing inputs,
not invented fields or zero resource use. It does not assert that supplied values
are in valid domains, edition-compatible or clinically coherent.

For admitted care, principal diagnosis alone does not establish AR-DRG: retain
additional diagnoses, procedures, age, sex, care type and other required inputs
for the selected licensed grouper/version. Historical class codes must not be
relabeled as current classes merely because their spelling matches.

Primary path: exact edition-compatible official maps and qualified provider.
Alternative: explicitly provisional coarse diagnosis summaries, without full
AECC/DRG or patient cost claims. Probabilistic mapping requires validated training
pairs and propagated uncertainty. Unmapped records remain included in inventory.
No licensed asset or patient record is committed here.

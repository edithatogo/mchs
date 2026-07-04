"""Public clinical dataset inventory for worked examples.

The records in this module are deliberately metadata-only. They describe
access, license, provenance, and suitability for tutorials, but they do not
download or bundle patient-level data.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

__all__ = [
    "PublicClinicalDatasetCandidate",
    "list_public_dataset_candidates",
    "select_initial_worked_example",
]

InitialRole = Literal[
    "primary",
    "deferred-ed-track",
    "deferred-interop",
    "comparison-synthetic",
]


@dataclass(frozen=True, slots=True)
class PublicClinicalDatasetCandidate:
    """Metadata-only public dataset suitability record."""

    dataset_id: str
    name: str
    version: str
    url: str
    doi: str | None
    citation: str
    license_name: str
    access_policy: str
    required_credentials: str
    redistribution_rules: str
    download_path: str
    file_size: str
    update_cadence: str
    clinical_fields: tuple[str, ...]
    fit_for_nwau_examples: str
    initial_role: InitialRole
    committed_fixture_use: str
    local_download_use: str
    docs_use: str
    runtime_example_use: str
    pros: tuple[str, ...]
    cons: tuple[str, ...]
    risks: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable candidate record."""
        return asdict(self)


def list_public_dataset_candidates() -> tuple[PublicClinicalDatasetCandidate, ...]:
    """Return the curated candidate list for public worked examples."""
    return (
        PublicClinicalDatasetCandidate(
            dataset_id="mimic-iv-demo-2.2",
            name="MIMIC-IV Clinical Database Demo",
            version="2.2",
            url="https://physionet.org/content/mimic-iv-demo/2.2/",
            doi="https://doi.org/10.13026/dp1f-ex47",
            citation=(
                "Johnson, A., Bulgarelli, L., Pollard, T., Horng, S., "
                "Celi, L. A., & Mark, R. (2023). MIMIC-IV Clinical "
                "Database Demo (version 2.2). PhysioNet. RRID:SCR_007345."
            ),
            license_name="Open Data Commons Open Database License v1.0",
            access_policy="open-access",
            required_credentials="none for direct PhysioNet file access",
            redistribution_rules=(
                "Raw files are open under ODbL terms but remain local-only in "
                "this repo; commit only metadata, manifests, and synthetic tiny "
                "fixtures."
            ),
            download_path="https://physionet.org/files/mimic-iv-demo/2.2/",
            file_size="15.5 MB uncompressed; 15.4 MB ZIP",
            update_cadence="versioned PhysioNet release; current version 2.2",
            clinical_fields=(
                "admissions",
                "patients",
                "diagnoses_icd",
                "procedures_icd",
                "drgcodes",
                "transfers",
                "icu_stays",
            ),
            fit_for_nwau_examples="admitted-episode-staging",
            initial_role="primary",
            committed_fixture_use="tiny synthetic MIMIC-shaped CSV fixtures only",
            local_download_use="supported through user-supplied local cache path",
            docs_use="primary tutorial dataset with fail-closed AR-DRG caveats",
            runtime_example_use="local ETL and synthetic-overlay calculator demo",
            pros=(
                "Open-access 100-patient subset with hospital and ICU tables.",
                "Contains admissions, diagnosis/procedure, and DRG metadata.",
                "Small enough for a local tutorial without bundling raw files.",
            ),
            cons=(
                "US MIMIC DRG and ICD fields are not Australian classifications.",
                "Authoritative NWAU requires local AR-DRG provenance or a "
                "clearly synthetic overlay.",
            ),
            risks=(
                "Overclaiming Australian AR-DRG/NWAU support from US data.",
                "Accidentally committing raw deidentified patient-level files.",
            ),
        ),
        PublicClinicalDatasetCandidate(
            dataset_id="mimic-iv-ed-demo-2.2",
            name="MIMIC-IV-ED Demo",
            version="2.2",
            url="https://physionet.org/content/mimic-iv-ed-demo/2.2/",
            doi="https://doi.org/10.13026/jzz5-vs76",
            citation=(
                "Johnson, A., Bulgarelli, L., Pollard, T., Celi, L. A., "
                "Horng, S., & Mark, R. (2023). MIMIC-IV-ED Demo "
                "(version 2.2). PhysioNet. RRID:SCR_007345."
            ),
            license_name="Open Data Commons Open Database License v1.0",
            access_policy="open-access",
            required_credentials="none for direct PhysioNet file access",
            redistribution_rules="Keep raw CSV files local-only; commit metadata only.",
            download_path="https://physionet.org/files/mimic-iv-ed-demo/2.2/",
            file_size="111.8 KB uncompressed; 95.5 KB ZIP",
            update_cadence="versioned PhysioNet release; current version 2.2",
            clinical_fields=(
                "edstays",
                "diagnosis",
                "medrecon",
                "pyxis",
                "triage",
                "vitalsign",
            ),
            fit_for_nwau_examples="emergency-workflow-candidate",
            initial_role="deferred-ed-track",
            committed_fixture_use="future tiny synthetic ED-shaped fixtures",
            local_download_use="future ED tutorial local cache",
            docs_use="future ED example after AECC/UDG scope is separated",
            runtime_example_use="deferred",
            pros=("Open-access ED-specific demo linked to MIMIC-IV Demo subjects.",),
            cons=("ED classification and NWAU workflow differs from acute admitted.",),
            risks=("Bundling ED scope would make the first acute tutorial too broad.",),
        ),
        PublicClinicalDatasetCandidate(
            dataset_id="mimic-iv-demo-meds-0.0.1",
            name="MIMIC-IV demo data in the Medical Event Data Standard",
            version="0.0.1",
            url="https://physionet.org/content/mimic-iv-demo-meds/0.0.1/",
            doi="https://doi.org/10.13026/t2y8-ea41",
            citation=(
                "van de Water, R. P., Steinberg, E., Wornow, M., "
                "Rockenschaub, P., & McDermott, M. (2025). MIMIC-IV demo "
                "data in the Medical Event Data Standard (version 0.0.1). "
                "PhysioNet. RRID:SCR_007345."
            ),
            license_name="Open Data Commons Open Database License v1.0",
            access_policy="open-access",
            required_credentials="none for direct PhysioNet file access",
            redistribution_rules="Keep Parquet event streams local-only.",
            download_path="https://physionet.org/files/mimic-iv-demo-meds/0.0.1/",
            file_size="5.7 MB uncompressed; 4.7 MB ZIP",
            update_cadence="versioned PhysioNet release; current version 0.0.1",
            clinical_fields=(
                "event_stream",
                "codes",
                "subject_splits",
                "dataset_metadata",
            ),
            fit_for_nwau_examples="interop-and-event-stream-candidate",
            initial_role="deferred-interop",
            committed_fixture_use="future tiny synthetic MEDS-shaped fixtures",
            local_download_use="future interop tutorial local cache",
            docs_use="future event-stream interoperability example",
            runtime_example_use="deferred",
            pros=("Useful for event-stream and ML-style interoperability patterns.",),
            cons=("Less direct for admitted-episode staging than relational CSVs.",),
            risks=("Would add a second data model to the first tutorial.",),
        ),
        PublicClinicalDatasetCandidate(
            dataset_id="mimic-iv-fhir-demo-2.1.0",
            name="MIMIC-IV Clinical Database Demo on FHIR",
            version="2.1.0",
            url="https://physionet.org/content/mimic-iv-fhir-demo/2.1.0/",
            doi="https://doi.org/10.13026/vphg-y548",
            citation=(
                "Bennett, A., Ulrich, H., Wiedekopf, J., Szul, P., "
                "Grimes, J., & Johnson, A. (2025). MIMIC-IV Clinical "
                "Database Demo on FHIR (version 2.1.0). PhysioNet. "
                "RRID:SCR_007345."
            ),
            license_name="Open Data Commons Open Database License v1.0",
            access_policy="open-access",
            required_credentials="none for direct PhysioNet file access",
            redistribution_rules="Keep NDJSON resources local-only.",
            download_path="https://physionet.org/files/mimic-iv-fhir-demo/2.1.0/",
            file_size="49.5 MB uncompressed; 49.5 MB ZIP",
            update_cadence="versioned PhysioNet release; current version 2.1.0",
            clinical_fields=(
                "FHIR Patient",
                "FHIR Encounter",
                "FHIR Condition",
                "FHIR Procedure",
                "FHIR Observation",
            ),
            fit_for_nwau_examples="fhir-interop-candidate",
            initial_role="deferred-interop",
            committed_fixture_use="future tiny synthetic FHIR NDJSON fixtures",
            local_download_use="future FHIR tutorial local cache",
            docs_use="future FHIR/API boundary example",
            runtime_example_use="deferred",
            pros=("FHIR resources demonstrate API and interoperability boundaries.",),
            cons=("Requires FHIR parsing and mapping before episode staging.",),
            risks=("Could distract from calculator input provenance in phase one.",),
        ),
        PublicClinicalDatasetCandidate(
            dataset_id="synthea",
            name="Synthea synthetic patient records",
            version="current generator or SyntheticMass releases",
            url="https://github.com/synthetichealth/synthea",
            doi=None,
            citation="Synthea synthetic patient generator, MITRE.",
            license_name="Apache-2.0",
            access_policy="open-source synthetic-data generator",
            required_credentials="none",
            redistribution_rules="Synthetic outputs may be regenerated and curated.",
            download_path="https://synthea.mitre.org/downloads",
            file_size="varies by generated cohort; SyntheticMass archive is large",
            update_cadence="open-source releases and generated datasets",
            clinical_fields=(
                "FHIR Patient",
                "FHIR Encounter",
                "FHIR Condition",
                "FHIR Procedure",
                "FHIR Claim",
            ),
            fit_for_nwau_examples="synthetic-comparison",
            initial_role="comparison-synthetic",
            committed_fixture_use="safe candidate for generated synthetic fixtures",
            local_download_use="optional generated cohort",
            docs_use="comparison point for no-real-data examples",
            runtime_example_use="future synthetic-only end-to-end example",
            pros=("No real patient data and no deidentification disclosure risk.",),
            cons=("Not real clinical data and not an Australian funding dataset.",),
            risks=("May look more complete than real-data provenance examples.",),
        ),
    )


def select_initial_worked_example(
    candidates: tuple[PublicClinicalDatasetCandidate, ...],
) -> PublicClinicalDatasetCandidate:
    """Select the first worked-example dataset from assessed candidates."""
    if not candidates:
        raise ValueError("no public dataset candidates were provided")
    primary = [
        candidate for candidate in candidates if candidate.initial_role == "primary"
    ]
    if not primary:
        raise ValueError("no primary public dataset candidate was selected")
    if len(primary) > 1:
        raise ValueError("only one primary public dataset candidate is allowed")
    return primary[0]

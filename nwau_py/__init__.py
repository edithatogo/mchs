"""Tools for reproducing IHACPA National Weighted Activity Units.

Keep the package import light so utility modules such as provenance helpers can
be imported without pulling in optional scoring dependencies.
"""

from __future__ import annotations

from importlib import import_module

__all__ = [
    "ABSTRACTION_BOUNDARIES",
    "ABSTRACTION_BOUNDARY_INDEX",
    "ABSTRACTION_BOUNDARY_MATRIX",
    "ABSTRACTION_BOUNDARY_REGISTRY",
    "ABSTRACTION_DOCTRINE",
    "ABSTRACTION_DOCTRINE_BOUNDARIES",
    "ABSTRACTION_DOCTRINE_FORBIDDEN_SHORTCUTS",
    "ABSTRACTION_SURFACES",
    "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_ASSERTION_MODES",
    "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_ROWS",
    "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_TYPES",
    "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_VERSION_MATRIX",
    "EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS",
    "EMERGENCY_CLASSIFICATION_SOURCE_REFS",
    "EMERGENCY_CLASSIFICATION_SYSTEMS",
    "EMERGENCY_CLASSIFICATION_VERSION_MATRIX",
    "EMERGENCY_CODE_MAPPING_BUNDLE_SCHEMA_VERSION",
    "EMERGENCY_CODE_MAPPING_BUNDLE_VERSION_MATRIX",
    "EMERGENCY_CODE_MAPPING_VALIDATION_STATUSES",
    "EMERGENCY_GROUPER_COMPATIBILITY_STATES",
    "EMERGENCY_GROUPER_MAPPING_STAGES",
    "EMERGENCY_GROUPER_REFERENCE_TYPES",
    "EMERGENCY_GROUPER_SOURCE_MODES",
    "EMERGENCY_GROUPER_VERSION_MATRIX",
    "EMERGENCY_STREAMS",
    "EMERGENCY_TRANSITION_PERIODS",
    "NEC26",
    "NEC26_SOURCE",
    "NEC_BY_YEAR",
    "NEP26",
    "NEP26_SOURCE",
    "NEP_BY_YEAR",
    "ARDRGMappingAssetReference",
    "ARDRGMappingCompatibilityResult",
    "ARDRGMappingRecord",
    "ARDRGMappingRegistryError",
    "ARDRGParityFixtureCompatibilityResult",
    "ARDRGParityFixtureError",
    "ARDRGParityFixtureRecord",
    "AbstractionBoundary",
    "AbstractionBoundaryError",
    "AbstractionDependency",
    "AbstractionDoctrine",
    "AbstractionSurface",
    "ClassificationRequirement",
    "ClassificationValidationError",
    "ClassificationValidationResult",
    "CodingSetCompatibilityResult",
    "CodingSetFamily",
    "CodingSetPolicy",
    "CodingSetRegistryError",
    "CodingSetVersion",
    "DependencyKind",
    "EmergencyClassificationCompatibilityResult",
    "EmergencyClassificationParityFixtureCompatibilityResult",
    "EmergencyClassificationParityFixtureError",
    "EmergencyClassificationParityFixtureRecord",
    "EmergencyClassificationRecord",
    "EmergencyClassificationRegistryError",
    "EmergencyClassificationVersion",
    "EmergencyCodeMappingAssetReference",
    "EmergencyCodeMappingBundleCompatibilityResult",
    "EmergencyCodeMappingBundleRecord",
    "EmergencyCodeMappingDryRunSummary",
    "EmergencyCodeMappingPipelineError",
    "EmergencyGrouperCompatibilityResult",
    "EmergencyGrouperError",
    "EmergencyGrouperOutputRecord",
    "EmergencyGrouperProvenance",
    "EmergencyGrouperReference",
    "EmergencyGrouperVersionWindow",
    "EmergencyTransitionPeriod",
    "LicensedProductAssetReference",
    "LicensedProductCompatibilityResult",
    "LicensedProductManifestRecord",
    "LicensedProductWorkflowError",
    "abstraction_doctrine",
    "ar_drg_mapping_registry",
    "ar_drg_version_parity_fixtures",
    "build_ar_drg_parity_fixture_reference",
    "build_classification_requirement",
    "build_emergency_classification_parity_fixture_reference",
    "build_emergency_code_mapping_asset_reference",
    "build_emergency_code_mapping_bundle_record",
    "build_emergency_external_reference",
    "build_emergency_output_record_from_reference",
    "build_emergency_precomputed_output_record",
    "build_emergency_provenance",
    "build_licensed_product_asset_reference",
    "build_licensed_product_manifest_record",
    "classification_validation",
    "coding_set_registry",
    "describe_abstraction_doctrine",
    "diagnose_missing_licensed_assets",
    "emergency_classification_parity_fixtures",
    "emergency_code_mapping_pipeline",
    "emergency_grouper",
    "emergency_transition_registry",
    "ensure_ar_drg_mapping_compatibility",
    "ensure_ar_drg_parity_fixture_scope",
    "ensure_coding_set_compatibility",
    "ensure_commit_safe_exclusion",
    "ensure_emergency_classification_compatibility",
    "ensure_emergency_classification_parity_fixture_scope",
    "ensure_emergency_code_mapping_bundle_compatibility",
    "ensure_emergency_grouper_compatibility",
    "ensure_licensed_product_compatibility",
    "formula_parameter_bundle",
    "get_abstraction_boundary",
    "get_allowed_target_surfaces",
    "get_ar_drg_mapping_record",
    "get_ar_drg_parity_fixture_record",
    "get_classification_name",
    "get_classification_requirement",
    "get_classification_version",
    "get_coding_set_family",
    "get_coding_set_policy",
    "get_coding_set_restriction",
    "get_coding_set_version",
    "get_emergency_classification_name",
    "get_emergency_classification_parity_fixture_record",
    "get_emergency_classification_record",
    "get_emergency_classification_status",
    "get_emergency_classification_version",
    "get_emergency_code_mapping_bundle_record",
    "get_emergency_supported_years",
    "get_emergency_transition_period",
    "get_emergency_transition_years",
    "get_expected_ar_drg_version",
    "get_expected_classification_version",
    "get_expected_coding_set_version",
    "get_expected_coding_set_versions",
    "get_expected_emergency_classification_version",
    "get_licensed_product_manifest_record",
    "get_nec",
    "get_nep",
    "get_required_classification_fields",
    "get_supported_classification_years",
    "get_supported_coding_set_years",
    "get_supported_pricing_years",
    "get_transition_years",
    "is_classification_licensed",
    "is_coding_set_licensed",
    "is_coding_set_restricted",
    "is_commit_safe_excluded_path",
    "is_local_only_licensed_path",
    "licensed_product_workflow",
    "list_ar_drg_mapping_records",
    "list_ar_drg_parity_fixture_records",
    "list_coding_set_families",
    "list_emergency_classification_parity_fixture_records",
    "list_emergency_classification_records",
    "list_emergency_code_mapping_bundle_records",
    "list_emergency_transition_periods",
    "list_licensed_product_manifest_records",
    "normalize_classification_system",
    "normalize_emergency_classification_system",
    "register_ar_drg_local_licensed_parity_fixture_reference",
    "register_ar_drg_synthetic_parity_fixture",
    "register_emergency_local_official_classification_parity_fixture_reference",
    "register_emergency_synthetic_classification_parity_fixture",
    "resolve_licensed_product_env_path",
    "score_readmission",
    "summarize_emergency_code_mapping_dry_run",
    "validate_abstraction_boundary",
    "validate_abstraction_dependencies",
    "validate_abstraction_dependency",
    "validate_aecc_input",
    "validate_amhcc_input",
    "validate_ar_drg_input",
    "validate_ar_drg_mapping_compatibility",
    "validate_ar_drg_parity_fixture_scope",
    "validate_ar_drg_version_binding",
    "validate_classification_input",
    "validate_classification_version",
    "validate_coding_set_compatibility",
    "validate_emergency_classification_compatibility",
    "validate_emergency_classification_parity_fixture_scope",
    "validate_emergency_code_mapping_bundle_compatibility",
    "validate_emergency_grouper_compatibility",
    "validate_emergency_input",
    "validate_licensed_product_compatibility",
    "validate_required_classification_fields",
    "validate_tier_2_input",
    "validate_udg_input",
]

_LAZY_ATTRS = {
    "score_readmission": (".scoring", "score_readmission"),
    "abstraction_doctrine": (".abstraction_doctrine", None),
    "ABSTRACTION_BOUNDARIES": (".abstraction_doctrine", "ABSTRACTION_BOUNDARIES"),
    "ABSTRACTION_BOUNDARY_INDEX": (
        ".abstraction_doctrine",
        "ABSTRACTION_BOUNDARY_INDEX",
    ),
    "ABSTRACTION_BOUNDARY_MATRIX": (
        ".abstraction_doctrine",
        "ABSTRACTION_BOUNDARY_MATRIX",
    ),
    "ABSTRACTION_BOUNDARY_REGISTRY": (
        ".abstraction_doctrine",
        "ABSTRACTION_BOUNDARY_REGISTRY",
    ),
    "ABSTRACTION_DOCTRINE": (".abstraction_doctrine", "ABSTRACTION_DOCTRINE"),
    "ABSTRACTION_DOCTRINE_BOUNDARIES": (
        ".abstraction_doctrine",
        "ABSTRACTION_DOCTRINE_BOUNDARIES",
    ),
    "ABSTRACTION_DOCTRINE_FORBIDDEN_SHORTCUTS": (
        ".abstraction_doctrine",
        "ABSTRACTION_DOCTRINE_FORBIDDEN_SHORTCUTS",
    ),
    "ABSTRACTION_SURFACES": (".abstraction_doctrine", "ABSTRACTION_SURFACES"),
    "AbstractionBoundary": (".abstraction_doctrine", "AbstractionBoundary"),
    "AbstractionBoundaryError": (
        ".abstraction_doctrine",
        "AbstractionBoundaryError",
    ),
    "AbstractionDependency": (".abstraction_doctrine", "AbstractionDependency"),
    "AbstractionDoctrine": (".abstraction_doctrine", "AbstractionDoctrine"),
    "AbstractionSurface": (".abstraction_doctrine", "AbstractionSurface"),
    "DependencyKind": (".abstraction_doctrine", "DependencyKind"),
    "describe_abstraction_doctrine": (
        ".abstraction_doctrine",
        "describe_abstraction_doctrine",
    ),
    "get_abstraction_boundary": (".abstraction_doctrine", "get_abstraction_boundary"),
    "get_allowed_target_surfaces": (
        ".abstraction_doctrine",
        "get_allowed_target_surfaces",
    ),
    "validate_abstraction_boundary": (
        ".abstraction_doctrine",
        "validate_abstraction_boundary",
    ),
    "validate_abstraction_dependency": (
        ".abstraction_doctrine",
        "validate_abstraction_dependency",
    ),
    "validate_abstraction_dependencies": (
        ".abstraction_doctrine",
        "validate_abstraction_dependencies",
    ),
    "formula_parameter_bundle": (".formula_parameter_bundle", None),
    "get_nec": (".pricing_constants", "get_nec"),
    "get_nep": (".pricing_constants", "get_nep"),
    "get_supported_pricing_years": (
        ".pricing_constants",
        "get_supported_pricing_years",
    ),
    "NEC26": (".pricing_constants", "NEC26"),
    "NEC26_SOURCE": (".pricing_constants", "NEC26_SOURCE"),
    "NEC_BY_YEAR": (".pricing_constants", "NEC_BY_YEAR"),
    "NEP26": (".pricing_constants", "NEP26"),
    "NEP26_SOURCE": (".pricing_constants", "NEP26_SOURCE"),
    "NEP_BY_YEAR": (".pricing_constants", "NEP_BY_YEAR"),
    "coding_set_registry": (".coding_set_registry", None),
    "ar_drg_mapping_registry": (".ar_drg_mapping_registry", None),
    "ar_drg_version_parity_fixtures": (".ar_drg_version_parity_fixtures", None),
    "emergency_transition_registry": (".emergency_transition_registry", None),
    "emergency_classification_parity_fixtures": (
        ".emergency_classification_parity_fixtures",
        None,
    ),
    "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_ASSERTION_MODES": (
        ".emergency_classification_parity_fixtures",
        "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_ASSERTION_MODES",
    ),
    "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_ROWS": (
        ".emergency_classification_parity_fixtures",
        "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_ROWS",
    ),
    "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_TYPES": (
        ".emergency_classification_parity_fixtures",
        "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_TYPES",
    ),
    "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_VERSION_MATRIX": (
        ".emergency_classification_parity_fixtures",
        "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_VERSION_MATRIX",
    ),
    "EmergencyClassificationParityFixtureCompatibilityResult": (
        ".emergency_classification_parity_fixtures",
        "EmergencyClassificationParityFixtureCompatibilityResult",
    ),
    "EmergencyClassificationParityFixtureError": (
        ".emergency_classification_parity_fixtures",
        "EmergencyClassificationParityFixtureError",
    ),
    "EmergencyClassificationParityFixtureRecord": (
        ".emergency_classification_parity_fixtures",
        "EmergencyClassificationParityFixtureRecord",
    ),
    "build_emergency_classification_parity_fixture_reference": (
        ".emergency_classification_parity_fixtures",
        "build_emergency_classification_parity_fixture_reference",
    ),
    "ensure_emergency_classification_parity_fixture_scope": (
        ".emergency_classification_parity_fixtures",
        "ensure_emergency_classification_parity_fixture_scope",
    ),
    "get_emergency_classification_parity_fixture_record": (
        ".emergency_classification_parity_fixtures",
        "get_emergency_classification_parity_fixture_record",
    ),
    "list_emergency_classification_parity_fixture_records": (
        ".emergency_classification_parity_fixtures",
        "list_emergency_classification_parity_fixture_records",
    ),
    "register_emergency_local_official_classification_parity_fixture_reference": (
        ".emergency_classification_parity_fixtures",
        "register_emergency_local_official_classification_parity_fixture_reference",
    ),
    "register_emergency_synthetic_classification_parity_fixture": (
        ".emergency_classification_parity_fixtures",
        "register_emergency_synthetic_classification_parity_fixture",
    ),
    "validate_emergency_classification_parity_fixture_scope": (
        ".emergency_classification_parity_fixtures",
        "validate_emergency_classification_parity_fixture_scope",
    ),
    "emergency_code_mapping_pipeline": (".emergency_code_mapping_pipeline", None),
    "emergency_grouper": (".emergency_grouper", None),
    "EMERGENCY_GROUPER_REFERENCE_TYPES": (
        ".emergency_grouper",
        "EMERGENCY_GROUPER_REFERENCE_TYPES",
    ),
    "EMERGENCY_GROUPER_COMPATIBILITY_STATES": (
        ".emergency_grouper",
        "EMERGENCY_GROUPER_COMPATIBILITY_STATES",
    ),
    "EMERGENCY_GROUPER_MAPPING_STAGES": (
        ".emergency_grouper",
        "EMERGENCY_GROUPER_MAPPING_STAGES",
    ),
    "EMERGENCY_GROUPER_SOURCE_MODES": (
        ".emergency_grouper",
        "EMERGENCY_GROUPER_SOURCE_MODES",
    ),
    "EMERGENCY_GROUPER_VERSION_MATRIX": (
        ".emergency_grouper",
        "EMERGENCY_GROUPER_VERSION_MATRIX",
    ),
    "EmergencyGrouperCompatibilityResult": (
        ".emergency_grouper",
        "EmergencyGrouperCompatibilityResult",
    ),
    "EmergencyGrouperError": (".emergency_grouper", "EmergencyGrouperError"),
    "EmergencyGrouperOutputRecord": (
        ".emergency_grouper",
        "EmergencyGrouperOutputRecord",
    ),
    "EmergencyGrouperProvenance": (
        ".emergency_grouper",
        "EmergencyGrouperProvenance",
    ),
    "EmergencyGrouperReference": (
        ".emergency_grouper",
        "EmergencyGrouperReference",
    ),
    "EmergencyGrouperVersionWindow": (
        ".emergency_grouper",
        "EmergencyGrouperVersionWindow",
    ),
    "build_emergency_external_reference": (
        ".emergency_grouper",
        "build_emergency_external_reference",
    ),
    "build_emergency_output_record_from_reference": (
        ".emergency_grouper",
        "build_emergency_output_record_from_reference",
    ),
    "build_emergency_precomputed_output_record": (
        ".emergency_grouper",
        "build_emergency_precomputed_output_record",
    ),
    "build_emergency_provenance": (
        ".emergency_grouper",
        "build_emergency_provenance",
    ),
    "ensure_emergency_grouper_compatibility": (
        ".emergency_grouper",
        "ensure_emergency_grouper_compatibility",
    ),
    "EMERGENCY_CODE_MAPPING_BUNDLE_SCHEMA_VERSION": (
        ".emergency_code_mapping_pipeline",
        "EMERGENCY_CODE_MAPPING_BUNDLE_SCHEMA_VERSION",
    ),
    "EMERGENCY_CODE_MAPPING_BUNDLE_VERSION_MATRIX": (
        ".emergency_code_mapping_pipeline",
        "EMERGENCY_CODE_MAPPING_BUNDLE_VERSION_MATRIX",
    ),
    "EMERGENCY_CODE_MAPPING_VALIDATION_STATUSES": (
        ".emergency_code_mapping_pipeline",
        "EMERGENCY_CODE_MAPPING_VALIDATION_STATUSES",
    ),
    "EmergencyCodeMappingAssetReference": (
        ".emergency_code_mapping_pipeline",
        "EmergencyCodeMappingAssetReference",
    ),
    "EmergencyCodeMappingBundleCompatibilityResult": (
        ".emergency_code_mapping_pipeline",
        "EmergencyCodeMappingBundleCompatibilityResult",
    ),
    "EmergencyCodeMappingBundleRecord": (
        ".emergency_code_mapping_pipeline",
        "EmergencyCodeMappingBundleRecord",
    ),
    "EmergencyCodeMappingDryRunSummary": (
        ".emergency_code_mapping_pipeline",
        "EmergencyCodeMappingDryRunSummary",
    ),
    "EmergencyCodeMappingPipelineError": (
        ".emergency_code_mapping_pipeline",
        "EmergencyCodeMappingPipelineError",
    ),
    "build_emergency_code_mapping_asset_reference": (
        ".emergency_code_mapping_pipeline",
        "build_emergency_code_mapping_asset_reference",
    ),
    "build_emergency_code_mapping_bundle_record": (
        ".emergency_code_mapping_pipeline",
        "build_emergency_code_mapping_bundle_record",
    ),
    "ensure_emergency_code_mapping_bundle_compatibility": (
        ".emergency_code_mapping_pipeline",
        "ensure_emergency_code_mapping_bundle_compatibility",
    ),
    "get_emergency_code_mapping_bundle_record": (
        ".emergency_code_mapping_pipeline",
        "get_emergency_code_mapping_bundle_record",
    ),
    "list_emergency_code_mapping_bundle_records": (
        ".emergency_code_mapping_pipeline",
        "list_emergency_code_mapping_bundle_records",
    ),
    "summarize_emergency_code_mapping_dry_run": (
        ".emergency_code_mapping_pipeline",
        "summarize_emergency_code_mapping_dry_run",
    ),
    "validate_emergency_code_mapping_bundle_compatibility": (
        ".emergency_code_mapping_pipeline",
        "validate_emergency_code_mapping_bundle_compatibility",
    ),
    "CodingSetCompatibilityResult": (
        ".coding_set_registry",
        "CodingSetCompatibilityResult",
    ),
    "CodingSetFamily": (".coding_set_registry", "CodingSetFamily"),
    "CodingSetPolicy": (".coding_set_registry", "CodingSetPolicy"),
    "CodingSetRegistryError": (".coding_set_registry", "CodingSetRegistryError"),
    "CodingSetVersion": (".coding_set_registry", "CodingSetVersion"),
    "ARDRGMappingAssetReference": (
        ".ar_drg_mapping_registry",
        "ARDRGMappingAssetReference",
    ),
    "ARDRGMappingCompatibilityResult": (
        ".ar_drg_mapping_registry",
        "ARDRGMappingCompatibilityResult",
    ),
    "ARDRGMappingRecord": (".ar_drg_mapping_registry", "ARDRGMappingRecord"),
    "ARDRGMappingRegistryError": (
        ".ar_drg_mapping_registry",
        "ARDRGMappingRegistryError",
    ),
    "ARDRGParityFixtureCompatibilityResult": (
        ".ar_drg_version_parity_fixtures",
        "ARDRGParityFixtureCompatibilityResult",
    ),
    "ARDRGParityFixtureError": (
        ".ar_drg_version_parity_fixtures",
        "ARDRGParityFixtureError",
    ),
    "ARDRGParityFixtureRecord": (
        ".ar_drg_version_parity_fixtures",
        "ARDRGParityFixtureRecord",
    ),
    "EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS": (
        ".emergency_transition_registry",
        "EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS",
    ),
    "EMERGENCY_CLASSIFICATION_SOURCE_REFS": (
        ".emergency_transition_registry",
        "EMERGENCY_CLASSIFICATION_SOURCE_REFS",
    ),
    "EMERGENCY_CLASSIFICATION_SYSTEMS": (
        ".emergency_transition_registry",
        "EMERGENCY_CLASSIFICATION_SYSTEMS",
    ),
    "EMERGENCY_CLASSIFICATION_VERSION_MATRIX": (
        ".emergency_transition_registry",
        "EMERGENCY_CLASSIFICATION_VERSION_MATRIX",
    ),
    "EMERGENCY_STREAMS": (
        ".emergency_transition_registry",
        "EMERGENCY_STREAMS",
    ),
    "EMERGENCY_TRANSITION_PERIODS": (
        ".emergency_transition_registry",
        "EMERGENCY_TRANSITION_PERIODS",
    ),
    "EmergencyClassificationCompatibilityResult": (
        ".emergency_transition_registry",
        "EmergencyClassificationCompatibilityResult",
    ),
    "EmergencyClassificationRecord": (
        ".emergency_transition_registry",
        "EmergencyClassificationRecord",
    ),
    "EmergencyClassificationRegistryError": (
        ".emergency_transition_registry",
        "EmergencyClassificationRegistryError",
    ),
    "EmergencyClassificationVersion": (
        ".emergency_transition_registry",
        "EmergencyClassificationVersion",
    ),
    "EmergencyTransitionPeriod": (
        ".emergency_transition_registry",
        "EmergencyTransitionPeriod",
    ),
    "ensure_ar_drg_mapping_compatibility": (
        ".ar_drg_mapping_registry",
        "ensure_ar_drg_mapping_compatibility",
    ),
    "build_ar_drg_parity_fixture_reference": (
        ".ar_drg_version_parity_fixtures",
        "build_ar_drg_parity_fixture_reference",
    ),
    "ensure_ar_drg_parity_fixture_scope": (
        ".ar_drg_version_parity_fixtures",
        "ensure_ar_drg_parity_fixture_scope",
    ),
    "ensure_coding_set_compatibility": (
        ".coding_set_registry",
        "ensure_coding_set_compatibility",
    ),
    "ensure_emergency_classification_compatibility": (
        ".emergency_transition_registry",
        "ensure_emergency_classification_compatibility",
    ),
    "get_ar_drg_mapping_record": (
        ".ar_drg_mapping_registry",
        "get_ar_drg_mapping_record",
    ),
    "get_expected_ar_drg_version": (
        ".ar_drg_mapping_registry",
        "get_expected_ar_drg_version",
    ),
    "get_coding_set_family": (".coding_set_registry", "get_coding_set_family"),
    "get_coding_set_policy": (".coding_set_registry", "get_coding_set_policy"),
    "get_coding_set_restriction": (
        ".coding_set_registry",
        "get_coding_set_restriction",
    ),
    "get_coding_set_version": (".coding_set_registry", "get_coding_set_version"),
    "get_emergency_classification_name": (
        ".emergency_transition_registry",
        "get_emergency_classification_name",
    ),
    "get_emergency_classification_record": (
        ".emergency_transition_registry",
        "get_emergency_classification_record",
    ),
    "get_emergency_classification_version": (
        ".emergency_transition_registry",
        "get_emergency_classification_version",
    ),
    "get_emergency_classification_status": (
        ".emergency_transition_registry",
        "get_emergency_classification_status",
    ),
    "get_emergency_supported_years": (
        ".emergency_transition_registry",
        "get_emergency_supported_years",
    ),
    "get_emergency_transition_period": (
        ".emergency_transition_registry",
        "get_emergency_transition_period",
    ),
    "get_emergency_transition_years": (
        ".emergency_transition_registry",
        "get_emergency_transition_years",
    ),
    "get_expected_emergency_classification_version": (
        ".emergency_transition_registry",
        "get_expected_emergency_classification_version",
    ),
    "get_expected_coding_set_version": (
        ".coding_set_registry",
        "get_expected_coding_set_version",
    ),
    "get_expected_coding_set_versions": (
        ".ar_drg_mapping_registry",
        "get_expected_coding_set_versions",
    ),
    "get_ar_drg_parity_fixture_record": (
        ".ar_drg_version_parity_fixtures",
        "get_ar_drg_parity_fixture_record",
    ),
    "get_supported_coding_set_years": (
        ".coding_set_registry",
        "get_supported_coding_set_years",
    ),
    "is_coding_set_licensed": (".coding_set_registry", "is_coding_set_licensed"),
    "is_coding_set_restricted": (".coding_set_registry", "is_coding_set_restricted"),
    "list_ar_drg_mapping_records": (
        ".ar_drg_mapping_registry",
        "list_ar_drg_mapping_records",
    ),
    "list_ar_drg_parity_fixture_records": (
        ".ar_drg_version_parity_fixtures",
        "list_ar_drg_parity_fixture_records",
    ),
    "list_coding_set_families": (".coding_set_registry", "list_coding_set_families"),
    "list_emergency_classification_records": (
        ".emergency_transition_registry",
        "list_emergency_classification_records",
    ),
    "list_emergency_transition_periods": (
        ".emergency_transition_registry",
        "list_emergency_transition_periods",
    ),
    "normalize_emergency_classification_system": (
        ".emergency_transition_registry",
        "normalize_emergency_classification_system",
    ),
    "validate_ar_drg_mapping_compatibility": (
        ".ar_drg_mapping_registry",
        "validate_ar_drg_mapping_compatibility",
    ),
    "validate_ar_drg_parity_fixture_scope": (
        ".ar_drg_version_parity_fixtures",
        "validate_ar_drg_parity_fixture_scope",
    ),
    "validate_ar_drg_version_binding": (
        ".ar_drg_mapping_registry",
        "validate_ar_drg_version_binding",
    ),
    "validate_coding_set_compatibility": (
        ".coding_set_registry",
        "validate_coding_set_compatibility",
    ),
    "validate_emergency_classification_compatibility": (
        ".emergency_transition_registry",
        "validate_emergency_classification_compatibility",
    ),
    "validate_emergency_input": (
        ".emergency_transition_registry",
        "validate_emergency_input",
    ),
    "validate_emergency_grouper_compatibility": (
        ".emergency_grouper",
        "validate_emergency_grouper_compatibility",
    ),
    "classification_validation": (".classification_validation", None),
    "ClassificationRequirement": (
        ".classification_validation",
        "ClassificationRequirement",
    ),
    "ClassificationValidationError": (
        ".classification_validation",
        "ClassificationValidationError",
    ),
    "ClassificationValidationResult": (
        ".classification_validation",
        "ClassificationValidationResult",
    ),
    "build_classification_requirement": (
        ".classification_validation",
        "build_classification_requirement",
    ),
    "get_classification_name": (
        ".classification_validation",
        "get_classification_name",
    ),
    "get_classification_version": (
        ".classification_validation",
        "get_classification_version",
    ),
    "get_classification_requirement": (
        ".classification_validation",
        "get_classification_requirement",
    ),
    "get_expected_classification_version": (
        ".classification_validation",
        "get_expected_classification_version",
    ),
    "get_required_classification_fields": (
        ".classification_validation",
        "get_required_classification_fields",
    ),
    "get_supported_classification_years": (
        ".classification_validation",
        "get_supported_classification_years",
    ),
    "get_transition_years": (".classification_validation", "get_transition_years"),
    "is_classification_licensed": (
        ".classification_validation",
        "is_classification_licensed",
    ),
    "normalize_classification_system": (
        ".classification_validation",
        "normalize_classification_system",
    ),
    "validate_aecc_input": (
        ".classification_validation",
        "validate_aecc_input",
    ),
    "validate_amhcc_input": (".classification_validation", "validate_amhcc_input"),
    "validate_ar_drg_input": (".classification_validation", "validate_ar_drg_input"),
    "validate_classification_input": (
        ".classification_validation",
        "validate_classification_input",
    ),
    "validate_classification_version": (
        ".classification_validation",
        "validate_classification_version",
    ),
    "validate_required_classification_fields": (
        ".classification_validation",
        "validate_required_classification_fields",
    ),
    "validate_tier_2_input": (".classification_validation", "validate_tier_2_input"),
    "validate_udg_input": (
        ".classification_validation",
        "validate_udg_input",
    ),
    "licensed_product_workflow": (".licensed_product_workflow", None),
    "LicensedProductAssetReference": (
        ".licensed_product_workflow",
        "LicensedProductAssetReference",
    ),
    "LicensedProductCompatibilityResult": (
        ".licensed_product_workflow",
        "LicensedProductCompatibilityResult",
    ),
    "LicensedProductManifestRecord": (
        ".licensed_product_workflow",
        "LicensedProductManifestRecord",
    ),
    "LicensedProductWorkflowError": (
        ".licensed_product_workflow",
        "LicensedProductWorkflowError",
    ),
    "build_licensed_product_asset_reference": (
        ".licensed_product_workflow",
        "build_licensed_product_asset_reference",
    ),
    "build_licensed_product_manifest_record": (
        ".licensed_product_workflow",
        "build_licensed_product_manifest_record",
    ),
    "diagnose_missing_licensed_assets": (
        ".licensed_product_workflow",
        "diagnose_missing_licensed_assets",
    ),
    "ensure_commit_safe_exclusion": (
        ".licensed_product_workflow",
        "ensure_commit_safe_exclusion",
    ),
    "ensure_licensed_product_compatibility": (
        ".licensed_product_workflow",
        "ensure_licensed_product_compatibility",
    ),
    "get_licensed_product_manifest_record": (
        ".licensed_product_workflow",
        "get_licensed_product_manifest_record",
    ),
    "is_commit_safe_excluded_path": (
        ".licensed_product_workflow",
        "is_commit_safe_excluded_path",
    ),
    "is_local_only_licensed_path": (
        ".licensed_product_workflow",
        "is_local_only_licensed_path",
    ),
    "list_licensed_product_manifest_records": (
        ".licensed_product_workflow",
        "list_licensed_product_manifest_records",
    ),
    "resolve_licensed_product_env_path": (
        ".licensed_product_workflow",
        "resolve_licensed_product_env_path",
    ),
    "validate_licensed_product_compatibility": (
        ".licensed_product_workflow",
        "validate_licensed_product_compatibility",
    ),
    "register_ar_drg_synthetic_parity_fixture": (
        ".ar_drg_version_parity_fixtures",
        "register_ar_drg_synthetic_parity_fixture",
    ),
    "register_ar_drg_local_licensed_parity_fixture_reference": (
        ".ar_drg_version_parity_fixtures",
        "register_ar_drg_local_licensed_parity_fixture_reference",
    ),
}


def __getattr__(name: str):
    """Lazily expose heavyweight public symbols on demand."""
    target = _LAZY_ATTRS.get(name)
    if target is not None:
        module_name, attr_name = target
        module = import_module(module_name, __name__)
        return module if attr_name is None else getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

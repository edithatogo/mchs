"""Calculator entry points and contract types."""

from __future__ import annotations

from importlib import import_module

__all__ = [
    "CMTY_MH_ARTIFACTS",
    "COMMUNITY_MH_CONTRACT",
    "AcuteCalculationContract",
    "AcuteContractError",
    "AcuteInputContract",
    "AcuteParams",
    "AcuteReferenceBundle",
    "CommunityMHArtifact",
    "CommunityMHCalculator",
    "CommunityMHContractError",
    "CommunityMHParams",
    "EDParams",
    "MHParams",
    "OutpatientParams",
    "SubacuteParams",
    "build_acute_contract",
    "build_community_mh_contract",
    "build_formula_program_from_steps",
    "calculate_acute",
    "calculate_acute_rust_2025",
    "calculate_adjusted_nwau",
    "calculate_community_mh",
    "calculate_ed",
    "calculate_funding",
    "calculate_mh",
    "calculate_outpatients",
    "calculate_subacute",
    "get_active_years",
    "get_inventory_by_year",
    "get_shadow_years",
    "load_formula",
    "load_weights",
    "normalize_formula_document",
    "validate_acute_input_frame",
    "validate_community_mh_input",
    "validate_community_mh_output",
]

_LAZY_ATTRS = {
    "AcuteCalculationContract": (".acute", "AcuteCalculationContract"),
    "AcuteContractError": (".acute", "AcuteContractError"),
    "AcuteInputContract": (".acute", "AcuteInputContract"),
    "AcuteParams": (".acute", "AcuteParams"),
    "AcuteReferenceBundle": (".acute", "AcuteReferenceBundle"),
    "build_acute_contract": (".acute", "build_acute_contract"),
    "calculate_acute": (".acute", "calculate_acute"),
    "calculate_acute_rust_2025": (".acute", "calculate_acute_rust_2025"),
    "validate_acute_input_frame": (".acute", "validate_acute_input_frame"),
    "calculate_adjusted_nwau": (".adjust", "calculate_adjusted_nwau"),
    "CommunityMHCalculator": (".community_mh_calculator", "CommunityMHCalculator"),
    "CommunityMHParams": (".community_mh_calculator", "CommunityMHParams"),
    "calculate_community_mh": (".community_mh_calculator", "calculate_community_mh"),
    "COMMUNITY_MH_CONTRACT": (".community_mh_contract", "COMMUNITY_MH_CONTRACT"),
    "CommunityMHContractError": (
        ".community_mh_contract",
        "CommunityMHContractError",
    ),
    "build_community_mh_contract": (
        ".community_mh_contract",
        "build_community_mh_contract",
    ),
    "validate_community_mh_input": (
        ".community_mh_contract",
        "validate_community_mh_input",
    ),
    "validate_community_mh_output": (
        ".community_mh_contract",
        "validate_community_mh_output",
    ),
    "CMTY_MH_ARTIFACTS": (".community_mh_inventory", "CMTY_MH_ARTIFACTS"),
    "CommunityMHArtifact": (".community_mh_inventory", "CommunityMHArtifact"),
    "get_active_years": (".community_mh_inventory", "get_active_years"),
    "get_inventory_by_year": (".community_mh_inventory", "get_inventory_by_year"),
    "get_shadow_years": (".community_mh_inventory", "get_shadow_years"),
    "EDParams": (".ed", "EDParams"),
    "calculate_ed": (".ed", "calculate_ed"),
    "calculate_funding": (".funding_formula", "calculate_funding"),
    "build_formula_program_from_steps": (
        ".formula_ir",
        "build_formula_program_from_steps",
    ),
    "load_formula": (".funding_formula", "load_formula"),
    "normalize_formula_document": (
        ".formula_ir",
        "normalize_formula_document",
    ),
    "load_weights": (".funding_formula", "load_weights"),
    "MHParams": (".mh", "MHParams"),
    "calculate_mh": (".mh", "calculate_mh"),
    "OutpatientParams": (".outpatients", "OutpatientParams"),
    "calculate_outpatients": (".outpatients", "calculate_outpatients"),
    "SubacuteParams": (".subacute", "SubacuteParams"),
    "calculate_subacute": (".subacute", "calculate_subacute"),
}


def __getattr__(name: str):
    """Lazily expose calculator symbols on demand."""
    target = _LAZY_ATTRS.get(name)
    if target is not None:
        module_name, attr_name = target
        module = import_module(module_name, __name__)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

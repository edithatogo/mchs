from nwau_py.grouping_readiness import AECC_INPUTS, assess_aecc_inputs


def test_absent_attributes_are_not_inferred_from_dates_or_referral():
    result = assess_aecc_inputs(
        {
            "principal_diagnosis": "synthetic",
            "age": 0,
            "triage_category": 3,
            "departure_date": "2026-01-01",
            "referral_source": "GP",
        },
        diagnosis_mapping_qualified=False,
    )
    assert result.missing_inputs == (
        "arrival_transport",
        "clinical_care_commencement",
        "episode_end_status",
    )
    assert result.mapping_unresolved
    assert not result.input_inventory_complete


def test_complete_inventory_is_not_grouper_qualification():
    result = assess_aecc_inputs(
        dict.fromkeys(AECC_INPUTS, 1), diagnosis_mapping_qualified=True
    )
    assert result.input_inventory_complete
    assert not result.official_grouping_qualified


def test_blank_is_missing_but_zero_is_observed():
    values = dict.fromkeys(AECC_INPUTS, 0)
    values["principal_diagnosis"] = " "
    assert assess_aecc_inputs(
        values, diagnosis_mapping_qualified=True
    ).missing_inputs == ("principal_diagnosis",)

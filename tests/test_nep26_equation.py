from decimal import Decimal

import pytest

from nwau_py.calculators.nep26_equation import TERMS, evaluate


def test_independent_nonzero_reference_and_currency_units():
    terms = dict.fromkeys(TERMS, Decimal(0))
    terms.update(
        PW=Decimal(2),
        APaed=Decimal("1.1"),
        AInd=Decimal(".1"),
        ARes=Decimal(".2"),
        ART=Decimal(".3"),
        ADia=Decimal(".4"),
        ATreat=Decimal(".5"),
        AICU=Decimal(".1"),
        ICU_hours=Decimal(10),
        APPS=Decimal(".1"),
        LOS=Decimal(2),
        AAcc=Decimal(".2"),
        AHAC=Decimal(".1"),
        PWAHR=Decimal(3),
        AAHR=Decimal(".1"),
        NEP=Decimal(7418),
    )
    result = evaluate(terms)
    # Hand calculation: 6.6 + 1 - .3 - .4 - .2 - .3 = 6.4.
    assert result.activity_nwau == Decimal("6.4")
    assert result.amount_aud == Decimal("47475.2")
    terms["APPS"] = Decimal(10)
    assert evaluate(terms).activity_nwau < 0  # no implicit funding floor


@pytest.mark.parametrize("bad", ["missing", "covid", "nonfinite"])
def test_invalid_inputs_rejected(bad):
    terms = dict.fromkeys(TERMS, Decimal(0))
    if bad == "missing":
        del terms["APaed"]
    elif bad == "covid":
        terms["AC19"] = Decimal(0)
    else:
        terms["PW"] = Decimal("NaN")
    with pytest.raises(ValueError):
        evaluate(terms)

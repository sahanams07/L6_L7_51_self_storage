import pytest
from self_storage import rent_due, access_allowed, payment_status


# ---------- rent_due ----------
def test_within_deposit_months():
    assert rent_due("small", 1, False, False) == 0

def test_unknown_unit_size():
    with pytest.raises(ValueError):
        rent_due("huge", 3, False, False)

def test_negative_months():
    with pytest.raises(ValueError):
        rent_due("small", -1, False, False)

def test_member_bonus_climate():
    # medium covers 2 + 1 member month = 3, extra = 2, climate rate 120
    assert rent_due("medium", 5, True, True) == 240

def test_standard_rate_no_climate():
    # small covers 1, extra = 4, rate 80
    assert rent_due("small", 5, False, False) == 320

def test_long_stay_discount_no_climate():
    # extra = 9 (>6), rate 80 - 10 = 70
    assert rent_due("small", 10, False, False) == 630

def test_long_stay_discount_climate():
    # extra = 9 (>6), rate 120 - 10 - 5 = 105
    assert rent_due("small", 10, True, False) == 945


# ---------- access_allowed ----------
def test_access_allowed():
    assert access_allowed(12, 1, False) is True

def test_owner_access():
    assert access_allowed(3, 4, True) is True

def test_non_owner_outside_hours():
    assert access_allowed(5, 1, False) is False


# ---------- payment_status ----------
def test_status_current():
    assert payment_status(10, False, False) == "current"

def test_status_grace():
    assert payment_status(0, False, False) == "grace"

def test_status_lien():
    assert payment_status(-30, False, False) == "lien"

def test_autopay_and_prior_late():
    assert payment_status(10, True, True) == "current"

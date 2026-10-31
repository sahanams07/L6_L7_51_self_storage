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

def test_zero_months_not_negative():
    # months = 0 is valid (months < 0 is False) and extra <= 0
    assert rent_due("small", 0, False, False) == 0

def test_member_non_large_gets_bonus_month():
    # is_member True and unit_size != "large" -> covered 2+1 = 3, extra 2
    assert rent_due("medium", 5, False, True) == 160

def test_member_large_no_bonus_month():
    # is_member True but unit_size == "large" -> covered stays 3, extra 2
    assert rent_due("large", 5, False, True) == 160

def test_non_member_no_bonus_month():
    # is_member False -> covered 1, extra 4
    assert rent_due("small", 5, False, False) == 320

def test_climate_rate_short_stay():
    # climate rate 120, extra 2 (not > 6)
    assert rent_due("small", 3, True, False) == 240

def test_non_climate_rate_short_stay():
    assert rent_due("small", 3, False, False) == 160

def test_extra_exactly_six_no_discount():
    # boundary: extra == 6 -> extra > 6 is False
    assert rent_due("small", 7, False, False) == 480

def test_long_stay_discount_no_climate():
    # extra 9 > 6 -> rate 70
    assert rent_due("small", 10, False, False) == 630

def test_long_stay_discount_climate():
    # extra 9 > 6 -> rate 120 - 10 - 5 = 105
    assert rent_due("small", 10, True, False) == 945


# ---------- access_allowed ----------
def test_owner_within_limit():
    assert access_allowed(3, 4, True) is True

def test_owner_over_limit():
    assert access_allowed(12, 5, True) is False

def test_non_owner_too_early():
    assert access_allowed(5, 1, False) is False

def test_non_owner_too_late():
    assert access_allowed(23, 1, False) is False

def test_non_owner_open_hours_within_visitors():
    assert access_allowed(12, 2, False) is True

def test_non_owner_open_hours_too_many_visitors():
    assert access_allowed(12, 3, False) is False

def test_non_owner_boundary_hours():
    assert access_allowed(6, 1, False) is True
    assert access_allowed(22, 1, False) is True


# ---------- payment_status ----------
def test_autopay_current():
    assert payment_status(0, True, False) == "current"

def test_non_autopay_current():
    assert payment_status(5, False, False) == "current"

def test_prior_late_raises_cutoff():
    # cutoff 5 + 10 = 15
    assert payment_status(14, False, True) == "grace"
    assert payment_status(15, False, True) == "current"

def test_autopay_prior_late():
    # cutoff 0 + 10 = 10
    assert payment_status(10, True, True) == "current"

def test_grace_period():
    assert payment_status(-1, True, False) == "grace"
    assert payment_status(-10, False, False) == "grace"

def test_lien():
    assert payment_status(-16, True, False) == "lien"
    assert payment_status(-11, False, False) == "lien"

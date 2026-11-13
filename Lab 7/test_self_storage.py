

import pytest
from hypothesis import given, strategies as st

from self_storage import parse_rental, duration_average, payable_rent


@given(
    unit=st.text(min_size=1).filter(lambda x: ":" not in x and x.strip() != ""),
    months=st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False)
)
def test_parse_rental_valid(unit, months):
    result = parse_rental(f"{unit}:{months}")
    assert result == (unit.strip().title(), months)


@pytest.mark.parametrize("value", [None, "", ":", "medium:", ":6", "abc"])
def test_parse_rental_invalid(value):
    with pytest.raises(ValueError):
        parse_rental(value)


@given(st.lists(st.integers(), min_size=1).map(
    lambda values: ",".join(map(str, values))
))
def test_duration_average_valid(value):
    numbers = [int(x) for x in value.split(",")]
    assert duration_average(value) == sum(numbers) // len(numbers)


@pytest.mark.parametrize("value", [None, "", "abc", "1,,2", "1,x"])
def test_duration_average_invalid(value):
    with pytest.raises(ValueError):
        duration_average(value)


@given(
    rent=st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False)
)
def test_payable_rent_valid(rent, discount):
    assert payable_rent(f"{rent}|{discount}") == max(rent * 1.18 - discount, 0)


@pytest.mark.parametrize("value", [None, "", "|", "abc|10", "100|abc"])
def test_payable_rent_invalid(value):
    with pytest.raises(ValueError):
        payable_rent(value)

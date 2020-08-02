import pytest

from .coins import return_coins


@pytest.mark.parametrize(
    "price,inserted,expected",
    [
        (3.14, 500, {200: 248, 50: 1, 20: 1, 10: 1, 5: 1, 1: 1}),
        (4, 5, {100: 1}),
        (1.12, 2, {50: 1, 20: 1, 10: 1, 5: 1, 2: 1, 1: 1}),  # the worst
        (3.14, 3, {}),
        (3.14, 3.14, {}),
    ],
)
def test_correct_change(price: float, inserted: float, expected: dict):
    assert return_coins(coffee_price=price, eur_inserted=inserted) == expected

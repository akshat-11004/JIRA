from calculator import add


def test_positive_numbers():
    assert add(2, 3) == 5


def test_negative_numbers():
    assert add(-2, 3) == 1


def test_zero():
    assert add(0, 0) == 0

import pytest
from calculator import divide


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 2, 5.0),
        (-10, 2, -5.0),
        (10, -2, -5.0),
        (-10, -2, 5.0),
        (5, 2, 2.5),
        (0, 5, 0.0),
        (7.5, 2.5, 3.0),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == pytest.approx(expected)


def test_divide_by_zero():
    with pytest.raises(
        ZeroDivisionError,
        match="Cannot divide by zero"
    ):
        divide(10, 0)

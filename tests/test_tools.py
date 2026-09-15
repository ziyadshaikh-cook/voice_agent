import pytest

from src.tools import calculate, get_current_time


def test_calculate_addition():
    assert calculate("2 + 2") == 4


def test_calculate_multiplication():
    assert calculate("3 * 4") == 12


def test_calculate_negative_number():
    assert calculate("-5 + 10") == 5


def test_calculate_rejects_unsafe_input():
    with pytest.raises(ValueError):
        calculate("__import__('os').system('echo hi')")


def test_calculate_rejects_non_numeric_names():
    with pytest.raises(ValueError):
        calculate("some_variable + 1")


def test_get_current_time_returns_string():
    assert isinstance(get_current_time(), str)

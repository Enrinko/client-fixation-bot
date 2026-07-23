import pytest

from bot.phone import normalize_phone


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("+79161234567", "+79161234567"),
        ("79161234567", "+79161234567"),
        ("89161234567", "+79161234567"),
        ("9161234567", "+79161234567"),
        ("+7 (916) 123-45-67", "+79161234567"),
        ("8 916 123 45 67", "+79161234567"),
        ("8-916-123-45-67", "+79161234567"),
        ("84951234567", "+74951234567"),
        ("  +79161234567  ", "+79161234567"),
    ],
)
def test_valid_ru_numbers_normalize_to_plus7(raw: str, expected: str) -> None:
    assert normalize_phone(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        "",
        "   ",
        "abc",
        "позвонить вечером",
        "123",
        "91612345",
        "891612345678",
        "4951234567",
        "+19161234567",
        "+89161234567",
        "8916a123456",
        "тел. 89161234567",
        "8+9161234567",
    ],
)
def test_garbage_and_non_ru_numbers_are_rejected(raw: str) -> None:
    assert normalize_phone(raw) is None

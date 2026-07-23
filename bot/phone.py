"""Russian phone number normalization.

Accepted inputs (spaces, dashes and parentheses are ignored):
- +7XXXXXXXXXX / 7XXXXXXXXXX / 8XXXXXXXXXX — any RU area code;
- bare 10 digits only when they start with 9 (mobile), otherwise ambiguous.

Anything else — letters, foreign codes, wrong length — is rejected.
"""

import re

_ALLOWED_CHARS = re.compile(r"\+?[\d\s\-().]+")
_NON_DIGITS = re.compile(r"\D")


def normalize_phone(raw: str) -> str | None:
    """Return the number as +7XXXXXXXXXX, or None if the input is not a valid RU phone."""
    raw = raw.strip()
    if not _ALLOWED_CHARS.fullmatch(raw):
        return None

    digits = _NON_DIGITS.sub("", raw)

    if raw.startswith("+"):
        if len(digits) == 11 and digits[0] == "7":
            return f"+7{digits[1:]}"
        return None
    if len(digits) == 11 and digits[0] in "78":
        return f"+7{digits[1:]}"
    if len(digits) == 10 and digits[0] == "9":
        return f"+7{digits}"
    return None

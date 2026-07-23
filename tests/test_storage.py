from pathlib import Path

import pytest

from bot.storage import DuplicateClientError, LeadStorage


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "leads.db"


def test_lead_is_persisted_and_gets_an_id(db_path: Path) -> None:
    storage = LeadStorage(db_path)
    lead_id = storage.add_lead("+79161234567", "+79997654321", "Иванов Иван Иванович")
    assert lead_id == 1


def test_same_client_phone_twice_raises_duplicate_error(db_path: Path) -> None:
    storage = LeadStorage(db_path)
    storage.add_lead("+79161234567", "+79997654321", "Иванов Иван")
    with pytest.raises(DuplicateClientError):
        storage.add_lead("+79161234567", "+70000000000", "Другой Риелтор Тот Же Клиент")


def test_different_clients_are_both_stored(db_path: Path) -> None:
    storage = LeadStorage(db_path)
    first = storage.add_lead("+79161234567", "+79997654321", "Иванов Иван")
    second = storage.add_lead("+79161234568", "+79997654321", "Петров Пётр")
    assert first != second


def test_leads_survive_storage_reopen(db_path: Path) -> None:
    LeadStorage(db_path).add_lead("+79161234567", "+79997654321", "Иванов Иван")
    reopened = LeadStorage(db_path)
    with pytest.raises(DuplicateClientError):
        reopened.add_lead("+79161234567", "+79997654321", "Иванов Иван")

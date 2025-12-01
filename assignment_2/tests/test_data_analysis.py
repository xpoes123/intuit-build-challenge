import sys
from pathlib import Path
from decimal import Decimal

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from assignment_2.data_analysis import (
    _load_transactions,
    total_revenue,
    revenue_for_category,
    TransactionRecord,
    Category,
)


def _get_csv_path() -> Path:
    return REPO_ROOT / "assignment_2" / "data" / "transactions.csv"


def test_load_transactions_parses_rows() -> None:
    csv_path = _get_csv_path()
    records = _load_transactions(csv_path)

    assert len(records) == 5

    first = records[0]
    assert isinstance(first, TransactionRecord)

    assert first.transaction_id == "T1001"
    assert first.user_id == "U001"
    assert first.category is Category.DIGITAL
    assert first.item == "Premium Upgrade"
    assert first.quantity == 1
    assert first.unit_price == Decimal("4.99")

    assert first.timestamp.year == 2025
    assert first.timestamp.month == 1
    assert first.timestamp.tzinfo is not None


def test_total_revenue_matches_manual_sum() -> None:
    csv_path = _get_csv_path()
    records = _load_transactions(csv_path)
    expected = (
        Decimal("4.99")
        + Decimal("7.50")
        + Decimal("9.99")
        + Decimal("4.95")
        + Decimal("6.40")
    )

    result = total_revenue(records)
    assert isinstance(result, Decimal)
    assert result == expected


def test_total_revenue_on_empty_iterable_is_zero() -> None:
    empty_records: list[TransactionRecord] = []
    result = total_revenue(empty_records)
    assert result == Decimal("0")


def test_revenue_for_category_digital_only() -> None:
    csv_path = _get_csv_path()
    records = _load_transactions(csv_path)

    expected = Decimal("4.99") + Decimal("4.95")

    result = revenue_for_category(records, Category.DIGITAL)
    assert result == expected

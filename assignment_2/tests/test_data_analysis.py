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
    revenue_by_category,
    revenue_by_user,
    top_n_items_by_revenue,
    average_revenue_per_user,
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



def test_revenue_by_category_matches_manual() -> None:
    csv_path = _get_csv_path()
    records = _load_transactions(csv_path)

    totals = revenue_by_category(records)

    assert totals[Category.DIGITAL] == Decimal("9.94")
    assert totals[Category.PHYSICAL] == Decimal("13.90")
    assert totals[Category.SUBSCRIPTION] == Decimal("9.99")


def test_revenue_by_user_matches_manual() -> None:
    csv_path = _get_csv_path()
    records = _load_transactions(csv_path)

    totals = revenue_by_user(records)

    assert totals["U001"] == Decimal("14.98")
    assert totals["U002"] == Decimal("13.90")
    assert totals["U003"] == Decimal("4.95")


def test_top_n_items_by_revenue() -> None:
    csv_path = _get_csv_path()
    records = _load_transactions(csv_path)

    top3 = top_n_items_by_revenue(records, n=3)
    assert top3 == [
        ("Monthly Plan", Decimal("9.99")),
        ("Notebook", Decimal("7.50")),
        ("Pen Set", Decimal("6.40")),
    ]


def test_top_n_items_by_revenue_with_large_n() -> None:
    csv_path = _get_csv_path()
    records = _load_transactions(csv_path)

    top10 = top_n_items_by_revenue(records, n=10)

    assert len(top10) == 5
    assert top10[0][0] == "Monthly Plan"
    assert top10[-1][0] == "Coin Pack"


def test_average_revenue_per_user_matches_manual() -> None:
    csv_path = _get_csv_path()
    records = _load_transactions(csv_path)

    averages = average_revenue_per_user(records)

    assert averages["U001"] == Decimal("7.49")
    assert averages["U002"] == Decimal("6.95")
    assert averages["U003"] == Decimal("4.95")


def test_load_transactions_missing_required_column_raises(tmp_path: Path) -> None:
    bad_csv = tmp_path / "bad_transactions.csv"
    bad_csv.write_text(
        "transaction_id,timestamp,user_id,category,item,quantity\n"
        "T1,2025-01-01T00:00:00Z,U001,digital,Something,1\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as excinfo:
        _ = _load_transactions(bad_csv)

    assert "missing required columns" in str(excinfo.value)


def test_load_transactions_unknown_category_raises(tmp_path: Path) -> None:
    bad_csv = tmp_path / "bad_category.csv"
    bad_csv.write_text(
        "transaction_id,timestamp,user_id,category,item,quantity,unit_price\n"
        "T1,2025-01-01T00:00:00Z,U001,invalid_category,Something,1,1.00\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as excinfo:
        _ = _load_transactions(bad_csv)

    assert "Unknown category" in str(excinfo.value)

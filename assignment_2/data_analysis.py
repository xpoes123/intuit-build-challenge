from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from os import PathLike
from collections.abc import Iterable
from decimal import Decimal
from enum import StrEnum
from collections import defaultdict

import csv


class Category(StrEnum):
    DIGITAL = "digital"
    PHYSICAL = "physical"
    SUBSCRIPTION = "subscription"


REQUIRED_COLUMNS = {
    "transaction_id",
    "timestamp",
    "user_id",
    "category",
    "item",
    "quantity",
    "unit_price",
}

PathTypes = str | Path | PathLike[str]


@dataclass(frozen=True, kw_only=True)
class TransactionRecord:
    transaction_id: str
    timestamp: datetime
    user_id: str
    category: Category
    item: str
    quantity: int
    unit_price: Decimal

    @property
    def revenue(self) -> Decimal:
        return self.quantity * self.unit_price


def _parse_timestamp(time_stamp: str) -> datetime:
    if time_stamp.endswith("Z"):
        time_stamp = time_stamp.replace("Z", "+00:00")
    return datetime.fromisoformat(time_stamp)


def _load_transactions(path: PathTypes) -> list[TransactionRecord]:
    csv_path = Path(path)

    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError(f"CSV file {csv_path} has no header row")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(
                f"CSV file {csv_path} is missing required columns: {sorted(missing)}"
            )

        records: list[TransactionRecord] = []
        for idx, row in enumerate(reader, start=2):
            category_value = row["category"]
            try:
                category = Category(category_value)
            except ValueError as exc:
                raise ValueError(
                    f"Unknown category '{category_value}' in row {idx} of {csv_path}"
                ) from exc

            record = TransactionRecord(
                transaction_id=row["transaction_id"],
                timestamp=_parse_timestamp(row["timestamp"]),
                user_id=row["user_id"],
                category=category,
                item=row["item"],
                quantity=int(row["quantity"]),
                unit_price=Decimal(row["unit_price"]),
            )
            records.append(record)

    return records


def total_revenue(records: Iterable[TransactionRecord]) -> Decimal:
    return sum((r.revenue for r in records), start=Decimal("0"))


def revenue_for_category(
    records: Iterable[TransactionRecord], category: Category
) -> Decimal:
    return sum(
        (r.revenue for r in records if r.category is category),
        start=Decimal("0"),
    )
    

def revenue_by_category(records: Iterable[TransactionRecord]) -> dict[Category, Decimal]:
    totals: dict[Category, Decimal] = defaultdict(lambda: Decimal("0"))
    for r in records:
        totals[r.category] += r.revenue
    return dict(totals)


def revenue_by_user(records: Iterable[TransactionRecord]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for r in records:
        totals[r.user_id] += r.revenue
    return dict(totals)


def top_n_items_by_revenue(
    records: Iterable[TransactionRecord],
    n: int = 3,
) -> list[tuple[str, Decimal]]:
    item_totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for r in records:
        item_totals[r.item] += r.revenue

    sorted_items = sorted(
        item_totals.items(),
        key=lambda kv: kv[1],
        reverse=True,
    )
    return sorted_items[:n]


def average_revenue_per_user(records: Iterable[TransactionRecord]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    counts: dict[str, int] = defaultdict(int)

    for r in records:
        totals[r.user_id] += r.revenue
        counts[r.user_id] += 1

    return {
        user: (totals[user] / counts[user]).quantize(Decimal("0.01"))
        for user in totals
    }


def main() -> None:
    csv_path = Path(__file__).resolve().parent / "data" / "transactions.csv"
    records = _load_transactions(csv_path)

    print("=== Assignment 2: Transaction Analysis ===")
    print(f"Loaded {len(records)} transactions from {csv_path.name}\n")

    total = total_revenue(records)
    print(f"Total revenue: {total}")

    by_cat = revenue_by_category(records)
    print("\nRevenue by category:")
    for cat, value in by_cat.items():
        print(f"  {cat.value}: {value}")

    physical_total = revenue_for_category(records, Category.PHYSICAL)
    print(f"\nRevenue for PHYSICAL only: {physical_total}")

    by_user = revenue_by_user(records)
    print("\nRevenue by user:")
    for user_id, value in by_user.items():
        print(f"  {user_id}: {value}")

    avg_by_user = average_revenue_per_user(records)
    print("\nAverage revenue per user:")
    for user_id, value in avg_by_user.items():
        print(f"  {user_id}: {value}")

    top_items = top_n_items_by_revenue(records, n=3)
    print("\nTop 3 items by revenue:")
    for item, value in top_items:
        print(f"  {item}: {value}")


if __name__ == "__main__":
    main()
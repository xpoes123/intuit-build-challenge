from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from os import PathLike
from collections.abc import Iterable
from decimal import Decimal
from enum import StrEnum

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
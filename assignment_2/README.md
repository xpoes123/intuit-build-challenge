# 📊 Intuit Build Challenge — Assignment 2
### CSV Transaction Analysis with Production Python Practices

This repository contains my solution to **Assignment 2** of the Intuit Build Challenge.
The goal is to implement a **transaction data analysis system** that demonstrates:

- Robust CSV parsing and validation
- Financial calculations with decimal precision
- Type-safe data modeling
- Clean functional design
- Comprehensive testing with edge cases

This implementation is written in **Python 3.11+** using modern Python features and production-grade practices for data integrity, type safety, and maintainability.

---

## 🚀 Project Structure

```
assignment_2/
│
├── data_analysis.py          # Core analysis functions + data model
├── data/
│   └── transactions.csv      # Sample transaction data
├── tests/
│   └── test_data_analysis.py # Comprehensive test suite
└── __init__.py

pyproject.toml                # Build + tooling config
.github/workflows/tests.yml   # CI: pytest + mypy
README.md                     # This file
```

---

# 🧠 Design Overview

## 1. **Type-Safe Data Model**

The `TransactionRecord` dataclass provides:

- **Immutability** via `frozen=True` (prevents accidental mutation)
- **Keyword-only arguments** for clarity at call sites
- **Computed properties** for derived values like revenue
- **Strong typing** with modern Python 3.11+ syntax

```python
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
```

This design prevents common bugs by making data transformations explicit and trackable.

---

## 2. **Decimal Precision for Financial Data**

**Critical production practice**: All monetary calculations use `Decimal` instead of `float`.

```python
unit_price: Decimal  # NOT float
```

Why this matters:
- Avoids floating-point precision errors (`0.1 + 0.2 ≠ 0.3` in float)
- Ensures accurate financial calculations
- Complies with accounting standards
- Prevents rounding errors in aggregations

This is a **must-have** in any production financial system.

---

## 3. **StrEnum for Type-Safe Categories**

Uses Python 3.11's `StrEnum` for category validation:

```python
class Category(StrEnum):
    DIGITAL = "digital"
    PHYSICAL = "physical"
    SUBSCRIPTION = "subscription"
```

Benefits:
- Type-safe comparisons using identity checks (`category is Category.DIGITAL`)
- Automatic serialization to strings
- IDE autocomplete support
- Prevents typos and invalid values

---

## 4. **Robust CSV Parsing with Validation**

The `_load_transactions()` function implements production-grade parsing:

### ✅ **Column Validation**
```python
REQUIRED_COLUMNS = {
    "transaction_id", "timestamp", "user_id",
    "category", "item", "quantity", "unit_price"
}

missing = REQUIRED_COLUMNS - set(reader.fieldnames)
if missing:
    raise ValueError(f"CSV missing required columns: {sorted(missing)}")
```

### ✅ **Category Validation**
```python
try:
    category = Category(category_value)
except ValueError as exc:
    raise ValueError(
        f"Unknown category '{category_value}' in row {idx} of {csv_path}"
    ) from exc
```

### ✅ **ISO 8601 Timestamp Parsing**
```python
def _parse_timestamp(time_stamp: str) -> datetime:
    if time_stamp.endswith("Z"):
        time_stamp = time_stamp.replace("Z", "+00:00")
    return datetime.fromisoformat(time_stamp)
```

This ensures timezone-aware datetimes for global applications.

---

## 5. **Flexible Path Handling**

Uses a **type alias** to accept multiple path types:

```python
PathTypes = str | Path | PathLike[str]

def _load_transactions(path: PathTypes) -> list[TransactionRecord]:
    csv_path = Path(path)  # Normalize to Path
```

This provides a user-friendly API while maintaining type safety.

---

## 6. **Efficient Aggregation Patterns**

### **Generator Expressions with `sum()`**

```python
def total_revenue(records: Iterable[TransactionRecord]) -> Decimal:
    return sum((r.revenue for r in records), start=Decimal("0"))
```

- Memory-efficient (doesn't build intermediate lists)
- Clean, functional style
- Explicit `Decimal("0")` start value prevents type coercion

### **defaultdict for Grouping**

```python
def revenue_by_category(records: Iterable[TransactionRecord]) -> dict[Category, Decimal]:
    totals: dict[Category, Decimal] = defaultdict(lambda: Decimal("0"))
    for r in records:
        totals[r.category] += r.revenue
    return dict(totals)  # Convert back to plain dict
```

Returns a plain `dict` rather than `defaultdict` to prevent accidental key creation in calling code.

---

## 7. **Clean Separation of Concerns**

The module structure separates:

1. **Data Loading** (`_load_transactions`) — prefixed with `_` to indicate internal use
2. **Analysis Functions** — pure functions accepting iterables
3. **Presentation** (`main()`) — orchestrates loading and output

This makes functions:
- Easily testable (just pass in data)
- Reusable in different contexts
- Composable for complex analyses

---

# 📚 Setup & Usage

### **Install dependencies**

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"   # Install with dev dependencies
```

---

## ▶️ Running the Analysis

Inside the repo root:

```bash
python -m assignment_2.data_analysis
```

Expected output:

```
=== Assignment 2: Transaction Analysis ===
Loaded 5 transactions from transactions.csv

Total revenue: 33.83

Revenue by category:
  digital: 9.94
  physical: 13.90
  subscription: 9.99

Revenue for PHYSICAL only: 13.90

Revenue by user:
  U001: 14.98
  U002: 13.90
  U003: 4.95

Average revenue per user:
  U001: 7.49
  U002: 6.95
  U003: 4.95

Top 3 items by revenue:
  Monthly Plan: 9.99
  Notebook: 7.50
  Pen Set: 6.40
```

---

## 🧪 Running Tests

```bash
pytest assignment_2/tests/ -v
```

To run type-checking:

```bash
mypy assignment_2
```

GitHub CI runs both automatically for every pull request.

---

# ✔ Test Coverage

The test suite demonstrates production testing practices:

### **Data Loading**
- ✅ Successful CSV parsing
- ✅ Type validation (enums, decimals, datetimes)
- ✅ Missing column detection
- ✅ Invalid category handling
- ✅ Error messages include row numbers for debugging

### **Revenue Calculations**
- ✅ Total revenue matches manual sum
- ✅ Empty iterable returns `Decimal("0")`
- ✅ Category filtering works correctly
- ✅ Per-user aggregation

### **Aggregations**
- ✅ Revenue by category
- ✅ Revenue by user
- ✅ Top N items (with N > total items)
- ✅ Average revenue per user with rounding

### **Edge Cases**
- ✅ Uses `pytest.raises` for exception testing
- ✅ Uses `tmp_path` fixture for test file generation
- ✅ Tests boundary conditions (empty data, large N values)

---

# 🏭 Production Python Practices Demonstrated

This implementation showcases **12 production-grade patterns**:

### 1. **Modern Type Hints (PEP 604)**
```python
PathTypes = str | Path | PathLike[str]  # Union types with |
```

### 2. **Frozen Dataclasses**
```python
@dataclass(frozen=True, kw_only=True)  # Immutable, explicit
```

### 3. **StrEnum (Python 3.11+)**
```python
class Category(StrEnum):  # Type-safe string enums
```

### 4. **Decimal for Money**
```python
unit_price: Decimal  # Never float for currency
```

### 5. **pathlib over os.path**
```python
csv_path = Path(path)  # Modern path handling
```

### 6. **Generator Expressions**
```python
sum((r.revenue for r in records), start=Decimal("0"))  # Memory efficient
```

### 7. **Exception Chaining**
```python
raise ValueError("...") from exc  # Preserves stack trace
```

### 8. **Validation with Clear Errors**
```python
raise ValueError(f"Unknown category '{value}' in row {idx}")  # Actionable
```

### 9. **ISO 8601 Timestamps**
```python
datetime.fromisoformat(time_stamp)  # Timezone-aware
```

### 10. **Identity Checks for Enums**
```python
if r.category is Category.DIGITAL:  # Use 'is', not '=='
```

### 11. **defaultdict → dict Conversion**
```python
return dict(totals)  # Prevent accidental key creation
```

### 12. **Comprehensive Testing**
```python
pytest.raises, tmp_path, parametrization  # Production test patterns
```

---

# 🔧 Extensibility

The architecture supports real-world extensions:

### Add New Categories
```python
class Category(StrEnum):
    DIGITAL = "digital"
    PHYSICAL = "physical"
    SUBSCRIPTION = "subscription"
    RENTAL = "rental"  # Just add here
```

### Add New Analysis Functions
All functions accept `Iterable[TransactionRecord]`, so:
- Chain filters and aggregations
- Works with generators for huge datasets
- Can swap data sources (API, database, etc.)

### Add More Computed Properties
```python
@property
def tax(self) -> Decimal:
    return self.revenue * Decimal("0.08")
```

---

# 📝 Notes

- **No pandas dependency** — Uses standard library for clarity and portability
- **Type-safe throughout** — mypy-compatible with strict checking
- **Efficient aggregations** — Uses generators and single-pass algorithms
- **Clear error messages** — Includes row numbers and column names in validation errors
- **Idiomatic Python** — Follows PEP 8, modern Python style (3.11+)

---

# 💬 Author

David Jiang
GitHub: https://github.com/xpoes123

---
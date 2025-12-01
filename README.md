# 🚀 Intuit Build Challenge Submission

**Author**: David Jiang
**GitHub**: [@xpoes123](https://github.com/xpoes123)
**Language**: Python 3.11+

---

## 📋 Overview

This repository contains my complete submission for Intuit's Build Challenge, demonstrating proficiency in **concurrent programming**, **functional programming**, and **production-grade Python development practices**.

Both assignments are implemented with:
- ✅ Clean, type-safe architecture
- ✅ Comprehensive unit tests
- ✅ Modern Python 3.11+ features
- ✅ GitHub Actions CI/CD
- ✅ Production-ready error handling
- ✅ Detailed documentation

---

## 📂 Repository Structure

```
intuit-build-challenge/
├── assignment_1/              # Producer-Consumer with Thread Sync
│   ├── blocking_queue.py
│   ├── producer_consumer.py
│   ├── tests/
│   └── README.md             # Detailed docs for Assignment 1
│
├── assignment_2/              # CSV Data Analysis
│   ├── data_analysis.py
│   ├── data/
│   │   └── transactions.csv
│   ├── tests/
│   └── README.md             # Detailed docs for Assignment 2
│
├── .github/
│   └── workflows/
│       └── test.yml          # CI: pytest + mypy
│
├── pyproject.toml            # Project config + dependencies
└── README.md                 # This file
```

---

## 🎯 Assignment Summaries

### **Assignment 1: Producer-Consumer Pattern** 🧵
[📖 Detailed README](assignment_1/README.md)

**Objective**: Demonstrate thread synchronization and concurrent programming

**Implementation Highlights**:
- ✅ Custom `BlockingQueue[T]` using `threading.Lock` and `Condition`
- ✅ Proper wait/notify semantics with **while-loop guards** (no spurious wakeups)
- ✅ Timeout support using `time.monotonic()` (avoids clock drift)
- ✅ Sentinel-based shutdown pattern
- ✅ Generic type support for type safety
- ✅ Monitor-pattern synchronization (single lock)
- ✅ Comprehensive tests covering blocking behavior, timeouts, and concurrency

**Why It Matters**:
- No reliance on `queue.Queue` — demonstrates understanding of low-level primitives
- Correct handling of thread coordination under blocking conditions
- Production-ready error handling and clean shutdown

---

### **Assignment 2: CSV Data Analysis** 📊
[📖 Detailed README](assignment_2/README.md)

**Objective**: Demonstrate functional programming and data aggregation

**Implementation Highlights**:
- ✅ **Decimal precision** for financial calculations (avoids float errors)
- ✅ **Frozen dataclasses** for immutable data modeling
- ✅ **StrEnum** for type-safe category validation
- ✅ **Generator expressions** for memory-efficient aggregations
- ✅ Robust CSV validation (column checks, enum validation, error messages with row numbers)
- ✅ **ISO 8601 timestamp parsing** with timezone support
- ✅ Clean functional design (pure functions accepting iterables)
- ✅ Exception chaining for debugging (`raise ... from exc`)

**Why It Matters**:
- Uses `Decimal` instead of `float` for money — critical for production financial systems
- Validates all input data with actionable error messages
- Modern Python features (PEP 604 union types, StrEnum from 3.11)
- No pandas dependency — demonstrates mastery of standard library

---

## 🏭 Production Python Practices

This submission showcases **15+ production-grade patterns** across both assignments:

### **Type Safety & Immutability**
- Modern type hints (PEP 604: `str | Path | PathLike[str]`)
- Frozen dataclasses (`@dataclass(frozen=True, kw_only=True)`)
- Generic types (`BlockingQueue[T]`)
- mypy-compatible type annotations

### **Concurrency Correctness**
- Monitor pattern with single lock
- While-loop wait guards (prevents spurious wakeups)
- Monotonic time for timeouts
- Sentinel-based shutdown

### **Financial Data Integrity**
- `Decimal` for all monetary values
- Explicit rounding with `quantize()`
- No floating-point precision errors

### **Error Handling**
- Exception chaining (`from exc`)
- Validation at system boundaries
- Actionable error messages with context (row numbers, column names)
- File existence checks

### **Modern Python (3.11+)**
- StrEnum for string enumerations
- Union types with `|` operator
- Pattern matching ready (not needed here, but code is structured for it)
- pathlib over os.path

### **Testing Discipline**
- Edge cases (empty inputs, boundary conditions)
- Error paths (missing columns, invalid data)
- Concurrency tests (blocking, timeouts)
- pytest fixtures (`tmp_path` for file testing)

### **Code Organization**
- Clean separation of concerns
- Pure functions for testability
- Private functions prefixed with `_`
- No global state

---

## ⚙️ Setup & Installation

### **Prerequisites**
- Python 3.11 or higher
- pip (comes with Python)

### **Clone the Repository**
```bash
git clone https://github.com/xpoes123/intuit-build-challenge.git
cd intuit-build-challenge
```

### **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Install Dependencies**
```bash
pip install -e ".[dev]"
```

This installs:
- `pytest` for testing
- `mypy` for type checking

---

## 🧪 Running Tests

### **Run All Tests**
```bash
pytest -v
```

### **Run Assignment 1 Tests Only**
```bash
pytest assignment_1/tests/ -v
```

### **Run Assignment 2 Tests Only**
```bash
pytest assignment_2/tests/ -v
```

### **Run Type Checking**
```bash
mypy assignment_1 assignment_2
```

### **Run Both Tests and Type Checking (CI Equivalent)**
```bash
pytest -q && mypy assignment_1 assignment_2
```

---

## ▶️ Running the Programs

### **Assignment 1: Producer-Consumer Demo**
```bash
python -m assignment_1.producer_consumer
```

**Sample Output**:
```
Produced: [1, 2, 3]
Consumed: [1, 2, 3]
```

---

### **Assignment 2: Transaction Analysis**
```bash
python -m assignment_2.data_analysis
```

**Sample Output**:
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

## 🔄 Continuous Integration

GitHub Actions CI runs on every push and pull request:

- ✅ All tests across both assignments
- ✅ Type checking with mypy
- ✅ Python 3.11 environment

**Status**: ![CI Status](https://github.com/xpoes123/intuit-build-challenge/actions/workflows/test.yml/badge.svg)

See [.github/workflows/test.yml](.github/workflows/test.yml) for configuration.

---

## 📖 Detailed Documentation

Each assignment has its own comprehensive README:

- **[Assignment 1 README](assignment_1/README.md)** — Deep dive into concurrency primitives, blocking queue design, and thread synchronization patterns
- **[Assignment 2 README](assignment_2/README.md)** — Comprehensive guide to production Python practices, financial data handling, and functional programming patterns

---

## 🎓 Key Technical Decisions

### **Why Python 3.11+?**
- Modern type hint syntax (`|` for unions)
- StrEnum for type-safe string enums
- Performance improvements for production use
- Best-in-class type inference

### **Why Manual BlockingQueue Instead of queue.Queue?**
- Demonstrates understanding of low-level concurrency primitives
- Shows proper use of locks and condition variables
- Interview-ready implementation that explains "how it works"

### **Why Decimal Instead of Float?**
- Financial calculations require exact precision
- `0.1 + 0.2 == 0.3` is false with floats, true with Decimal
- Industry standard for accounting systems
- Prevents accumulation errors in aggregations

### **Why No External Libraries (pandas, etc.)?**
- Demonstrates mastery of Python standard library
- Keeps solution lightweight and dependency-free
- Shows ability to implement algorithms from first principles
- Easier to review and understand

### **Why Frozen Dataclasses?**
- Immutability prevents accidental state mutation
- Makes code easier to reason about
- Thread-safe by default
- Matches functional programming paradigm

---

## 📊 Test Coverage Summary

### **Assignment 1: Producer-Consumer**
- ✅ 10 tests covering queue operations, blocking behavior, and pipeline
- ✅ Timeout handling
- ✅ Concurrency edge cases
- ✅ Sentinel shutdown

### **Assignment 2: Data Analysis**
- ✅ 11 tests covering parsing, aggregations, and error handling
- ✅ Missing column detection
- ✅ Invalid data validation
- ✅ Edge cases (empty data, large N values)
- ✅ Decimal precision verification

**Total**: 21 comprehensive tests with 100% pass rate

---

## 🔧 Project Configuration

### **pyproject.toml**
Modern Python packaging standard with:
- Project metadata
- Dependency management
- pytest configuration
- mypy type-checking settings

### **Type Checking**
Configured for production-grade type safety:
```toml
[tool.mypy]
python_version = "3.11"
packages = ["assignment_1", "assignment_2"]
warn_return_any = true
warn_unused_configs = true
```

---

## 💡 What Makes This Submission Stand Out

1. **Production-Ready Code**: Not just "works" — follows industry best practices
2. **Type Safety**: Comprehensive type hints verified by mypy
3. **Financial Precision**: Proper Decimal usage for money calculations
4. **Robust Error Handling**: Validation with actionable error messages
5. **Clean Architecture**: Separation of concerns, pure functions, testable design
6. **Modern Python**: Uses latest features from Python 3.11+
7. **Comprehensive Testing**: 21 tests covering happy paths, edge cases, and error conditions
8. **CI/CD**: Automated testing on every commit
9. **Documentation**: Detailed READMEs explaining design decisions
10. **No Shortcuts**: Manual implementations demonstrate deep understanding

---

## 🏁 Conclusion

This submission demonstrates:

- ✅ Strong understanding of concurrent programming fundamentals
- ✅ Mastery of Python's functional programming capabilities
- ✅ Production-grade code quality and testing discipline
- ✅ Ability to make informed technical decisions
- ✅ Clear communication through documentation
- ✅ Professional software engineering practices

Both assignments are **fully functional, well-tested, and production-ready**.

---

## 📬 Contact

**David Jiang**
GitHub: [@xpoes123](https://github.com/xpoes123)

For questions about this submission, please open an issue in this repository.

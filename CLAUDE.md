# AGENTS.md  
**LLM Context + Behavior Guide for This Repository**

This document exists to give LLM agents (Claude, ChatGPT, etc.) the contextual grounding needed to correctly assist with this project.  
It describes the purpose of the repository, the architecture, the relevant constraints, and the rules an LLM agent must follow when generating suggestions or code.

---

## 🏗 Project Overview

This repository contains my solution for **Intuit’s Build Challenge – Assignment 1**, which requires implementing a classic **Producer–Consumer concurrency pipeline** using:

- Thread synchronization
- Blocking queues
- Lock/Condition variables (wait/notify)
- A clear separation between queue, producer, consumer, and pipeline orchestration logic
- Full unit tests
- GitHub Actions CI

The project is written in **Python 3.11+** with optional `mypy` typing support and `pytest` tests.

This repo is intentionally small, clean, and self-contained for evaluator readability.

---

## 📁 Directory Structure

intuit-build-challenge/
│
├── assignment_1/
│ ├── init.py
│ ├── blocking_queue.py
│ ├── producer_consumer.py
│ ├── tests/
│ │ └── test_blocking_queue.py
| | └── test_producer_consumer.py
│
├── .github/
│ └── workflows/
│ └── tests.yml
│
├── pyproject.toml
├── .gitignore
└── README.md


### `assignment_1/blocking_queue.py`
Contains the `BlockingQueue[T]` implementation.  
Eventually provides:
- bounded capacity  
- `put()` (blocking / timeout)  
- `get()` (blocking / timeout)  
- queue state helpers  
- thread-safe behavior using `threading.Lock` + `threading.Condition`

### `assignment_1/producer_consumer.py`
Contains:
- `Producer` thread class  
- `Consumer` thread class  
- `run_pipeline()` orchestration function  

Uses the queue to move items from a source iterable → consumer destination list with a sentinel for termination.

### `assignment_1/tests/`
Contains incremental tests for:
- queue structure
- queue behavior
- blocking semantics
- producer/consumer correctness
- pipeline behavior

Tests are intentionally written to appear in PRs as the code evolves.

### `.github/workflows/tests.yml`
Continuous integration workflow running:
- pytest  
- mypy  

On pushes to `main` and all PR branches.

---

## 🎯 Goals of This Repository

1. Provide a **clear, readable, interview-ready implementation**.
2. Demonstrate:
   - threading fundamentals  
   - correct condition variable usage  
   - safe concurrency patterns  
   - clean failure handling with a sentinel shutdown  
   - stepwise testing  
3. Show ability to:
   - organize a small Python project professionally  
   - write typed, testable, reproducible modules  
   - configure modern Python tooling (`pyproject.toml`)  
   - set up GitHub Actions CI  

This is not a production system; clarity and correctness matter more than micro-optimizations.

---

## 🤖 Instructions for LLM Agents Working on This Repo

When assisting with this repository, follow these rules:

### 1. **Preserve the existing architecture**
The code is intentionally modular:
- `BlockingQueue` contains *only* synchronization logic  
- `Producer` and `Consumer` do not embed queue internals  
- Tests evolve incrementally with each feature

Do not collapse modules or introduce unnecessary abstractions.

---

### 2. **Always respect Python typing (PEP 484 / 695 where relevant)**
Use:
```python
from typing import Generic, TypeVar, Deque, Optional
Avoid over-complex types unless needed.

3. Concurrency must use Condition Variables

Do NOT:

rewrite using queue.Queue

rewrite using async/await

rewrite using multiprocessing

Allowed:

threading.Lock

threading.Condition

wait(), notify(), notify_all()

4. Tests must stay readable and instructive

Tests should be small, fast, and deterministic.

Avoid:

sleeping for long durations

creating excessive thread counts

nondeterministic behavior

5. CI must remain minimal and reproducible

The CI configuration should:

run pytest

run mypy

install dependencies via pyproject.toml

Do not modify tool versions unless necessary.

6. Follow the repository’s coding style

Clean, explicit imports

Descriptive docstrings

Stable, predictable behavior

No clever hacks unless documented

🟦 Summary

This repository demonstrates:

Concurrent queue design

Thread synchronization

Structured testing

Clean Python package layout

CI integration

Professional engineering standards
# 📦 Intuit Build Challenge — Assignment 1  
### Producer–Consumer Pattern with Thread Synchronization (Python)

This repository contains my solution to **Assignment 1** of the Intuit Build Challenge.  
The goal is to implement a classic **producer–consumer pattern** using:

- Thread synchronization  
- Blocking queues  
- Wait/Notify (`Condition`)  
- Correct concurrent programming practices  
- Comprehensive unit tests  

This implementation is written in **Python 3.11+** and does **not** depend on any external concurrency utilities (e.g., `queue.Queue`) — everything is implemented manually to demonstrate understanding of locks, conditions, and thread interactions.

---

## 🚀 Project Structure

```
assignment_1/
│
├── blocking_queue.py         # Custom bounded blocking queue
├── producer_consumer.py      # Producer, Consumer, run_pipeline()
├── tests/
│   ├── test_blocking_queue.py
│   └── test_producer_consumer.py
└── __init__.py

pyproject.toml                # Build + tooling config
.github/workflows/tests.yml   # CI: pytest + mypy
README.md                     # This file
```

---

# 🧠 Design Overview

## 1. **BlockingQueue**  
A manually implemented bounded FIFO queue supporting:

- `put(item, timeout=None)`  
- `get(timeout=None)`  
- Proper blocking behavior via `Condition.wait()`  
- Timeout support  
- A single shared lock for correct monitor-style synchronization

Key correctness guarantees:

- Producers block when the queue is full  
- Consumers block when the queue is empty  
- Both operations wake exactly one corresponding waiter  
- Spurious wakeups are handled using **while-loops**, not **if**

This matches real production monitor patterns.

---

## 2. **Producer Thread**

The `Producer`:

- Iterates over a source iterable  
- Pushes each item into the queue  
- On *any* exception, still sends a **sentinel**  
- Designed so replacing the source with a generator or I/O stream is trivial

---

## 3. **Consumer Thread**

The `Consumer`:

- Continuously pulls from the queue  
- Appends items to a destination container  
- Stops cleanly when it reads the sentinel  
- Never busy-loops  
- Works with arbitrary item types (`Generic[T]`)

---

## 4. **Sentinel-Based Shutdown**

We use a unique `SENTINEL = object()` rather than a shared value like `None`:

- Guaranteed non-collision  
- Identity-checked (`is`) so no ambiguity  
- Clean, minimal shutdown logic  

---

## 5. **Pipeline Orchestration**

`run_pipeline(source, queue_size)` wires everything together:

```
source -> Producer -> BlockingQueue -> Consumer -> destination
```

This is the recommended entrypoint for testing the system end-to-end.

---

# 📚 Setup & Usage

### **Create venv + install tooling**

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt   # optional, if you add reqs later
```

---

## ▶️ Running the Pipeline Demo

Inside the repo root:

```bash
python -m assignment_1.producer_consumer
```

Expected sample output (simplified):

```
Produced:  [1, 2, 3]
Consumed:  [1, 2, 3]
```

---

## 🧪 Running Tests

```bash
pytest -q
```

To run type-checking:

```bash
mypy assignment_1
```

GitHub CI runs both automatically for every pull request.

---

# ✔ Test Coverage

The test suite covers:

### **BlockingQueue**
- Initial state  
- put/get basic behavior  
- Full queue blocking  
- Empty queue blocking  
- Timeout behavior  
- Thread-safety under concurrency  

### **Producer / Consumer**
- Proper initialization  
- Producer sends sentinel even on error  
- Consumer drains items  
- Consumer stops on sentinel  

### **Pipeline**
- Round-trip behavior on integers  
- Handling of `None`  
- Stress tests with small queue capacities  
- Empty input  

---

# 🔧 Extensibility

The architecture intentionally supports extension:

### Add More Producers
- Simply start additional `Producer` threads on the same queue  
- All safety properties continue to hold  

### Add More Consumers
- Add more `Consumer` threads  
- Behavior remains correct as long as producers send one sentinel per consumer  

### Swap Queue Implementation
- BlockingQueue is isolated behind a clean interface  
- Can be replaced by an I/O backed queue or a disk-based buffer  

---

# 📝 Notes

- All synchronization uses a **single lock** following the monitor pattern  
- Timeouts use `time.monotonic()` to avoid clock drift issues  
- Dataclasses are used for clarity  
- Implementation avoids noisy logging to keep deliverables clean  

---

# 💬 Author

David Jiang  
GitHub: https://github.com/xpoes123  

---

# 🏁 Summary

This project demonstrates:

- Correct concurrency primitives  
- Solid testing discipline  
- Clean, extensible design  
- CI-backed workflow  
- Clear documentation  

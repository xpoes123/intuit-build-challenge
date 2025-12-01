import os
import sys
from pathlib import Path
import threading
import time

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from assignment_1.blocking_queue import BlockingQueue

def test_queue_initial_state() -> None:
    queue = BlockingQueue[int](max_size=5)
    assert queue.size() == 0
    assert queue.capacity() == 5
    assert queue.is_empty() is True
    assert queue.is_full() is False
    

def test_queue_rejects_invalid_capacity() -> None:
    with pytest.raises(ValueError):
        BlockingQueue[int](max_size=0)
    with pytest.raises(ValueError):
        BlockingQueue[int](max_size=-1)
        

def test_queue_put_and_get_basic() -> None:
    queue = BlockingQueue[int](max_size=3)
    queue.put(1)
    queue.put(2)
    queue.put(3)
    
    assert queue.size() == 3
    assert queue.is_full() is True
    
    assert queue.get() == 1
    assert queue.get() == 2
    assert queue.size() == 1
    assert queue.is_full() is False
    
    queue.put(4)
    assert queue.size() == 2
    assert queue.get() == 3
    assert queue.get() == 4
    assert queue.is_empty() is True


def test_queue_blocks_get_when_empty_until_item_available() -> None:
    queue: BlockingQueue[int] = BlockingQueue(max_size=2)
    result: list[int] = []
    
    def consumer() -> None:
        item = queue.get()
        result.append(item)
    
    t = threading.Thread(target=consumer)
    t.start()
    
    time.sleep(0.05)
    assert result == []
    
    queue.put(42)
    
    t.join(timeout=1.0)
    assert result == [42]


def test_queue_blocks_put_when_full_until_space_avilable() -> None:
    queue: BlockingQueue[int] = BlockingQueue(max_size=1)
    queue.put(10)
    
    blocked = {"value": True}
    
    def producer() -> None:
        queue.put(20)
        blocked["value"] = False
    
    t = threading.Thread(target=producer)
    t.start()
    
    time.sleep(0.05)
    assert blocked["value"] is True
    
    assert queue.get() == 10
    
    t.join(timeout=1.0)
    assert blocked["value"] is False
    assert queue.get() == 20
    assert queue.is_empty() is True
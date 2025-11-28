import pytest
 
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
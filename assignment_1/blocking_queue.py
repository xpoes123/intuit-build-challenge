from collections import deque
from typing import Deque, Generic, TypeVar
import threading
import time
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass(kw_only=True)
class BlockingQueue(Generic[T]):
    max_size: int = 10
    
    _queue: Deque[T] = field(init=False, repr=False)
    _lock: threading.Lock = field(init=False, repr=False)
    _not_empty: threading.Condition = field(init=False, repr=False)
    _not_full: threading.Condition = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        if self.max_size <= 0:
            raise ValueError("max_size must be greater than 0")
        
        self._queue = deque()
        
        self._lock = threading.Lock()
        
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)
    
    def put(self, item: T, timeout: float | None = None) -> None:
        with self._not_full:
            if timeout is not None:
                end_time = time.monotonic() + timeout
            
            while len(self._queue) >= self.max_size:
                if timeout is None:
                    self._not_full.wait()
                else:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("put() timed out waiting for space in the queue")
                    self._not_full.wait(timeout=remaining)
            self._queue.append(item)
            
            self._not_empty.notify()
    
    def get(self, timeout: float | None = None) -> T:
        with self._not_empty:
            if timeout is not None:
                end_time = time.monotonic() + timeout
                
            while len(self._queue) == 0:
                if timeout is None:
                    self._not_empty.wait()
                else:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("get() timed out waiting for item")
                    self._not_empty.wait(timeout=remaining)
            item = self._queue.popleft()
            self._not_full.notify()
            return item

    def size(self) -> int:
        with self._lock:
            return len(self._queue)
    
    def capacity(self) -> int:
        return self.max_size
    
    def is_empty(self) -> bool:
        with self._lock:
            return len(self._queue) == 0
    
    def is_full(self) -> bool:
        with self._lock:
            return len(self._queue) >= self.max_size

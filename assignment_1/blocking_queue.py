from collections import deque
from typing import Deque, Generic, TypeVar

T = TypeVar('T')

class BlockingQueue(Generic[T]):
    def __init__(self, max_size: int = 10) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be greater than 0")
        
        self._max_size = max_size
        self._queue: Deque[T] = deque()
    
    def put(self, item: T) -> None:
        self._queue.append(item)
    
    def get(self) -> T:
        return self._queue.popleft()

    def size(self) -> int:
        return len(self._queue)
    
    def capacity(self) -> int:
        return self._max_size
    
    def is_empty(self) -> bool:
        return self.size() == 0
    
    def is_full(self) -> bool:
        return self.size() >= self.capacity()
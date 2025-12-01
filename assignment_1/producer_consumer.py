import threading
from dataclasses import dataclass, field
from typing import Generic, Iterable, List, TypeVar
from assignment_1.blocking_queue import BlockingQueue

T = TypeVar("T")

SENTINEL = object()

@dataclass(kw_only=True, eq=False)
class Producer(threading.Thread, Generic[T]):
    source: Iterable[T]
    queue: BlockingQueue[object]
    sentinel: object = SENTINEL
    name: str = "producer"
    
    def __post_init__(self) -> None:
        threading.Thread.__init__(self, name=self.name)
    
    def run(self) -> None:
        pass


@dataclass(kw_only=True, eq=False)
class Consumer(threading.Thread, Generic[T]):
    queue: object
    destination: List[T] = field(default_factory=list)
    sentinel: object = SENTINEL
    name: str = "consumer"
    
    def __post_init__(self) -> None:
        threading.Thread.__init__(self, name=self.name)
        
    def run(self) -> None:
        pass

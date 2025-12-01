import threading
from dataclasses import dataclass, field
from typing import Generic, Iterable, List, TypeVar, cast
from assignment_1.blocking_queue import BlockingQueue
import time

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
        try:
            for item in self.source:
                self.queue.put(item)
        finally:
            self.queue.put(self.sentinel)


@dataclass(kw_only=True, eq=False)
class Consumer(threading.Thread, Generic[T]):
    queue: BlockingQueue[object]
    destination: List[T] = field(default_factory=list)
    sentinel: object = SENTINEL
    name: str = "consumer"
    
    def __post_init__(self) -> None:
        threading.Thread.__init__(self, name=self.name)
        
    def run(self) -> None:
        while True:
            item = self.queue.get()
            
            if item is self.sentinel:
                break
            
            value = cast(T, item)
            self.destination.append(value)


def run_pipeline(source: Iterable[T], queue_size: int=10) -> List[T]:
    queue: BlockingQueue[object] = BlockingQueue(max_size=queue_size)
    destination: List[T] = []

    producer: Producer[T] = Producer(source=source, queue=queue, sentinel=SENTINEL)
    consumer: Consumer[T] = Consumer(queue=queue, destination=destination, sentinel=SENTINEL)

    start = time.perf_counter()
    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    return destination
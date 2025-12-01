import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from assignment_1.producer_consumer import Producer, Consumer, SENTINEL
from assignment_1.blocking_queue import BlockingQueue

def test_producer_init() -> None:
    queue: BlockingQueue = BlockingQueue(max_size=5)
    producer: Producer = Producer(source=[1, 2, 3], queue=queue)
    assert producer.source == [1, 2, 3]
    assert producer.sentinel is SENTINEL


def test_consumer_init() -> None:
    queue: BlockingQueue = BlockingQueue(max_size=5)
    consumer: Consumer = Consumer(queue=queue, destination=[])
    assert consumer.destination == []
    assert consumer.sentinel is SENTINEL


def test_producer_enqueues_items_and_sentinel() -> None:
    queue: BlockingQueue[object] = BlockingQueue(max_size=5)
    source = [1, 2, 3]
    
    producer: Producer[int] = Producer(source=source, queue=queue)
    producer.start()
    producer.join(timeout=1.0)
    
    assert queue.get() == 1
    assert queue.get() == 2
    assert queue.get() == 3
    assert queue.get() is SENTINEL
    
    assert queue.is_empty() is True
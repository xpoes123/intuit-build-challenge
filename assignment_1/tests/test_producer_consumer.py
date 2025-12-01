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
    consumer: Consumer = Consumer(queue=None, destination=[])
    assert consumer.destination == []
    assert consumer.sentinel is SENTINEL

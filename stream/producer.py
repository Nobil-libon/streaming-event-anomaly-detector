# producer.py

import time
import random
from datetime import datetime
from queue import Queue
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import (
    EVENT_INTERVAL,
    ANOMALY_CHANCE,
    SPIKE_MULTIPLIER,
    NORMAL_MIN_EVENTS,
    NORMAL_MAX_EVENTS
)
# Shared Queue
event_queue = Queue()


def generate_event(order_id):
    """
    Generate a single order event
    """
    return {
        "event": "order_placed",
        "order_id": f"ORD{order_id}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def producer():
    order_id = 1

    print("🚀 Producer Started...")

    while True:

        # Generate anomaly spike
        if random.random() < ANOMALY_CHANCE:

            print(f"\n🚨 ANOMALY DETECTED: Generating {SPIKE_MULTIPLIER} events 🚨")

            for _ in range(SPIKE_MULTIPLIER):

                event = generate_event(order_id)

                event_queue.put(event)

                print(f"[ANOMALY] {event}")

                order_id += 1

        else:
            event = generate_event(order_id)

            event_queue.put(event)

            print(f"[NORMAL] {event}")

            order_id += 1

        print(f"Queue Size: {event_queue.qsize()}")

        time.sleep(EVENT_INTERVAL)


if __name__ == "__main__":
    producer()
import time
import random

def generate_state():
    while True:
        yield 'CLOSED' if random.random() < 0.7 else 'OPEN'

def run_ds1_simulator(delay, callback, stop_event, print_lock):
        for state in generate_state():
            time.sleep(delay)
            with print_lock:
                callback(state)
            if stop_event.is_set():
                  break
              
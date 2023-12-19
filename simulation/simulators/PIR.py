import time
import random


def run_pir_simulator(delay, callback, stop_event, print_lock, settings, publish_event):
    for number in random_number():  # Initialize the generator
        time.sleep(delay)
        with print_lock:
            callback(number, settings, publish_event)
        if stop_event.is_set():
            break


def random_number():
    while True:
        yield random.choice([0, 1])

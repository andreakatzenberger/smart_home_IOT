import time
import random


def run_dpir1_simulator(delay, callback, stop_event):
    for number in random_number():  # Initialize the generator
        time.sleep(delay)
        callback(number)
        if stop_event.is_set():
            break


def random_number():
    while True:
        yield random.choice([0, 1])

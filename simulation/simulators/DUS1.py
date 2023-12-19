import time
import random


def run_dus1_simulator(delay, callback, stop_event, print_lock, settings, publish_event):
    for number in random_number():
        time.sleep(delay)
        with print_lock:
            callback(number, settings, publish_event)
        if stop_event.is_set():
            break


def random_number(initial_value=7, variability=3):
    distance = initial_value
    distance += random.randint(-variability, variability)
    yield distance

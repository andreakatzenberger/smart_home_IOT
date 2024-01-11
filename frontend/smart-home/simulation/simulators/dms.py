import time
import random


def generate_value():
    while True:
        state_changed = random.randint(-5, 5)
        result_str = ''.join((random.choice('1234567890') for i in range(4)))
        if state_changed < 0:
            continue
        yield result_str


def run_dms_simulator(delay, callback, stop_event, settings, publish_event):
    for generated_text in generate_value():
        time.sleep(delay)  # Delay between readings (adjust as needed)
        callback(generated_text, settings, publish_event)
        if stop_event.is_set():
            break
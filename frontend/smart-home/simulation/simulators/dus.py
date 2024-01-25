import time
import random


def generate_value():
    while True:
        motion_detected = random.randint(-5, 5)
        if motion_detected > 2:
            distance = random.randint(1, 200)
            yield distance


def run_dus_simulator(delay, callback, stop_event, settings, publish_event):
    for motion in generate_value():
        time.sleep(delay)  # Delay between readings (adjust as needed)
        callback(motion, settings, publish_event)
        if stop_event.is_set():
            break

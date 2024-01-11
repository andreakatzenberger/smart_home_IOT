import time
import random


def generate_value():
    while True:
        motion_detected = random.randint(-5, 5)
        ret_motion = True
        if motion_detected < 3:
            ret_motion = False
        yield ret_motion


def run_dpir_simulator(delay, callback, stop_event, settings, publish_event):
    for motion in generate_value():
        time.sleep(delay)  # Delay between readings (adjust as needed)
        callback(motion, settings, publish_event)
        if stop_event.is_set():
            break

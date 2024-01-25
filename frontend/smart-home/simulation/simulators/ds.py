import time
import random

def generate_value():

    while True:
        state_changed = random.randint(-5, 5)
        if state_changed < 3:
            current_state = True
        else:
            current_state = False

        yield current_state


def run_ds_simulator(delay, callback, stop_event, settings, publish_event, system_event):

    for motion in generate_value():
        time.sleep(delay)
        callback(motion, settings, publish_event, system_event)
        if stop_event.is_set():
            break

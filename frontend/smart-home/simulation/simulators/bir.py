import time
import random

    
def run_bir_simulator(delay, callback, stop_event, settings, publish_event):
    while True:
        buttons = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '#']
        random_button = random.choice(buttons)
        callback(random_button, settings, publish_event)
        time.sleep(delay)
        if stop_event.is_set():
            break
            
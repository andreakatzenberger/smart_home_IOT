import time
import random

def generate_value():
      while True:
        current_time = time.strftime("%H %M")
        yield current_time

              
def run_b4sd_simulator(delay, callback, stop_event, settings, publish_event, clock_event):
    is_empty = False
    for value in generate_value():
        # Delay between readings (adjust as needed)
        if clock_event.is_set():
            time.sleep(0.5)
            if is_empty:
                is_empty = False
                value = "    "
            else:
                is_empty = True
        else:
            time.sleep(delay)
        callback(value, settings, publish_event)
        if stop_event.is_set():
            break
            
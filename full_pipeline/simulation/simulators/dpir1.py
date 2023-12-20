import time
import random

def generate_values():
      while True:
        yield random.choice([0, 1])

      

def run_dpir1_simulator(delay, callback, stop_event, publish_event, settings):
        for number in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            if number == 1:
                  callback(number, publish_event, settings)
            if stop_event.is_set():
                  break
              
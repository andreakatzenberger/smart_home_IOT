import time
import random

def run_lcd_simulator(delay, callback, stop_event, settings, publish_event, msg):
    while True:
        callback(msg, settings, publish_event)
        time.sleep(delay)  
        if stop_event.is_set():
            break
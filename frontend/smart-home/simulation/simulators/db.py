import time
import random


def run_buzzer_simulator(callback, stop_event, settings, publish_event, clock_event, alarm_event):

    while True:
        if stop_event.is_set():
            break
        is_bb = clock_event.is_set() and settings['name'] == 'BB'
        if is_bb or alarm_event.is_set():
            print("BB on")
            callback(settings, publish_event)
        time.sleep(1)


        


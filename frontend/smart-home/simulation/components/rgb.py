
import threading
import time
from locks.print_lock import print_lock
from actuators.rgb import run
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json
from datetime import datetime, timedelta


rgb_batch = []
publish_data_counter = 0
publish_data_limit = 5

def publisher_task(event, rgb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with print_lock:
            local_batch = rgb_batch.copy()
            publish_data_counter = 0
            rgb_batch.clear()
        publish.multiple(local_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


def rgb_callback(settings, publish_event, button_pressed):

    global publish_data_counter, publish_data_limit
    new_color = 'none' 
    if button_pressed == '0':
            new_color = 'none'
    elif button_pressed == '1':
        new_color = 'white'
    elif button_pressed == '2':
        new_color = 'red'

    elif button_pressed == '3':
        new_color = 'green'

    elif button_pressed == '4':
        new_color = 'blue'
    elif button_pressed == '5':
        new_color = 'lightBlue'
    elif button_pressed == '6':
        new_color = 'purple'
    elif button_pressed == '7':
        new_color = 'yellow'
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    payload = {
        'measurement': 'RGB',
        'simulated': settings['simulated'],
        'runs_on': settings['runs_on'],
        'name': settings['name'],
        'value': new_color,
        '_time': formatted_time
    }
    with print_lock:
        rgb_batch.append(('rgb', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_rgb(settings, threads, stop_event, button_pressed):
        #ButtonsNames = ["LEFT",   "RIGHT",      "UP",       "DOWN",       "2",          "3",          "1",        "OK",        "4",         "5",         "6",         "7",         "8",          "9",        "*",         "0",        "#"]  # String list in same order as HEX list

        if settings['simulated']:
            dl_thread = threading.Thread(target = rgb_callback, args=( settings, publish_event, button_pressed))
            dl_thread.start()
            threads.append(dl_thread)
        else:
            red = settings["RED"]
            green = settings["GREEN"]
            blue = settings["BLUE"]
            
            dms_thread = threading.Thread(target=run, args=(rgb_callback, stop_event, settings, publish_event, red, green, blue, button_pressed))
            dms_thread.start()
            threads.append(dms_thread)

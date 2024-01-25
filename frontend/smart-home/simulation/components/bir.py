import threading
import time
from locks.print_lock import print_lock
from datetime import datetime, timedelta

from simulators.bir import run_bir_simulator
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json
bir_batch = []
publish_data_counter = 0
publish_data_limit = 3


def publisher_task(event, bir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with print_lock:
            local_pir_batch = bir_batch.copy()
            publish_data_counter = 0
            bir_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        event.clear()

def bir_callback(button_pressed, settings, publish_event):
    global publish_data_counter, publish_data_limit
    
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    payload = {
        'measurement': 'Button Pressed',
        'simulated': settings['simulated'],
        'runs_on': settings['runs_on'],
        'name': settings['name'],
        'value': button_pressed,
        '_time': formatted_time
    }
    publish.single('bir-button-pressed', json.dumps({'button': button_pressed}), hostname=HOSTNAME, port=PORT)

    with print_lock:
        bir_batch.append(('bir', json.dumps(payload), 0, True))
        publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, bir_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_bir(settings, threads, stop_event):
        if settings['simulated']:
            dpir_thread = threading.Thread(target=run_bir_simulator,
                                          args=(30, bir_callback, stop_event, settings, publish_event))
            dpir_thread.start()
            threads.append(dpir_thread)
        else:
            from actuators.bir import run
            pin = settings['pin']
            dpir_thread = threading.Thread(target=run,
                                          args=(bir_callback, stop_event, settings, publish_event))
            dpir_thread.start()
            threads.append(dpir_thread)

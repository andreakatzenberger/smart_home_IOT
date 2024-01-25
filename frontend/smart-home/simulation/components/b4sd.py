import threading
import time
from locks.print_lock import print_lock
from datetime import datetime, timedelta

from simulators.b4sd import run_b4sd_simulator
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json
b4sd_batch = []
publish_data_counter = 0
publish_data_limit = 5


def publisher_task(event, b4sd_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with print_lock:
            local_pir_batch = b4sd_batch.copy()
            publish_data_counter = 0
            b4sd_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        event.clear()

def b4sd_callback(value, settings, publish_event):
    global publish_data_counter, publish_data_limit
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    payload = {
        'measurement': 'B4SD Time',
        'simulated': settings['simulated'],
        'runs_on': settings['runs_on'],
        'name': settings['name'],
        'value': str(value),
        '_time': formatted_time
    }
    with print_lock:
        b4sd_batch.append(('b4sd', json.dumps(payload), 0, True))
        publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, b4sd_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_b4sd(settings, threads, stop_event, clock_event):
        if settings['simulated']:
            dpir_thread = threading.Thread(target=run_b4sd_simulator,
                                          args=(5, b4sd_callback, stop_event, settings, publish_event, clock_event))
            dpir_thread.start()
            threads.append(dpir_thread)
        else:
            from displays.b4sd import run
            pin = settings['pin']
            dpir_thread = threading.Thread(target=run,
                                          args=(b4sd_callback, stop_event, settings, publish_event, clock_event))
            dpir_thread.start()
            threads.append(dpir_thread)

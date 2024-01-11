
import threading
import time
from locks.print_lock import print_lock
from actuators.dl import run_light
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json
from datetime import datetime, timedelta


dht_batch = []
publish_data_counter = 0
publish_data_limit = 0

def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with print_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


def dl_callback(settings, publish_event):
    global publish_data_counter, publish_data_limit
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    payload = {
        'measurement': 'Light',
        'simulated': settings['simulated'],
        'runs_on': settings['runs_on'],
        'name': settings['name'],
        'value': 1,
        '_time': formatted_time
    }
    with print_lock:
        dht_batch.append(('dl', json.dumps(payload), 0, True))
        publish_data_counter += 1
    if settings['simulated']:
        print('Light is on')
        time.sleep(10)
        print('Light is off')
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    payload = {
        'measurement': 'Light',
        'simulated': settings['simulated'],
        'runs_on': settings['runs_on'],
        'name': settings['name'],
        'value': 0,
        '_time': formatted_time
    }

    with print_lock:
        dht_batch.append(('dl', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_dl(settings, threads, stop_event, code):
        if settings['simulated']:
            dl_thread = threading.Thread(target = dl_callback, args=( settings, publish_event))
            dl_thread.start()
            threads.append(dl_thread)
        else:
            pin =settings['pin']
            dms_thread = threading.Thread(target=run_light, args=(pin,dl_callback, stop_event, settings, publish_event))
            dms_thread.start()
            threads.append(dms_thread)


from simulators.pir import run_pir_simulator
import threading
import time
from locks.print_lock import print_lock
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json
from datetime import datetime, timedelta

dht_batch = []
publish_data_counter = 0
publish_data_limit = 0


def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with print_lock:
            local_pir_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        publish.single(local_pir_batch[0][0], local_pir_batch[0][1], hostname=HOSTNAME, port=PORT)
        event.clear()

def pir_callback(motion_detected, settings, publish_event):
    global publish_data_counter, publish_data_limit
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    print(motion_detected)
    if motion_detected:
        payload = {
            'measurement': 'Motion',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': 1,
            '_time': formatted_time
        }
        with print_lock:
            dht_batch.append(('pir', json.dumps(payload), 0, True))
            publish_data_counter += 1
        if publish_data_counter >= publish_data_limit:
            publish_event.set()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_pir(settings, threads, stop_event):
        if settings['simulated']:
            pir_thread = threading.Thread(target = run_pir_simulator, args=(15, pir_callback, stop_event, settings, publish_event))
            pir_thread.start()
            threads.append(pir_thread)

        else:
            from sensors.pir import detect_motion
            pin = settings['pin']
            pir_thread = threading.Thread(target=detect_motion, args=(pin, pir_callback,stop_event, settings, publish_event))
            pir_thread.start()
            threads.append(pir_thread)


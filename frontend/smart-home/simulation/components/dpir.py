import threading
import time
from locks.print_lock import print_lock
from datetime import datetime, timedelta

from simulators.dpir import run_dpir_simulator
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json
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
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        event.clear()

def dpir_callback(motion_detected, settings, publish_event):
    global publish_data_counter, publish_data_limit
    if motion_detected:
        current_datetime = datetime.now()

        adjusted_datetime = current_datetime - timedelta(hours=1)

        formatted_time = adjusted_datetime.isoformat()
        payload = {
            'measurement': 'Motion',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': 1,
            '_time': formatted_time
        }
        with print_lock:
            dht_batch.append(('dpir', json.dumps(payload), 0, True))
            publish_data_counter += 1
        if publish_data_counter >= publish_data_limit:
            publish_event.set()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_dpir(settings, threads, stop_event):
        if settings['simulated']:
            dpir_thread = threading.Thread(target=run_dpir_simulator,
                                          args=(10, dpir_callback, stop_event, settings, publish_event))
            dpir_thread.start()
            threads.append(dpir_thread)
        else:
            from sensors.pir import detect_motion
            pin = settings['pin']
            dpir_thread = threading.Thread(target=detect_motion,
                                          args=(pin, dpir_callback, stop_event, settings, publish_event))
            dpir_thread.start()
            threads.append(dpir_thread)


import threading
import time
from locks.print_lock import print_lock
from simulators.dus import run_dus_simulator
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json
from datetime import datetime, timedelta

dht_batch = []
publish_data_counter = 0
publish_data_limit = 2

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

def dus_callback(distance, settings, publish_event):
    global publish_data_counter, publish_data_limit
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    payload = {
            'measurement': 'Distance',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': distance,
            '_time': formatted_time
    }
    with print_lock:
        dht_batch.append(('dus', json.dumps(payload), 0, True))
        publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def run_dus(settings, threads, stop_event):
        if settings['simulated']:
            dus_thread = threading.Thread(target = run_dus_simulator, args=(5, dus_callback, stop_event, settings, publish_event))
            dus_thread.start()
            threads.append(dus_thread)
        else:
            from sensors.dus import detect_distance
            pin_trig = settings['pin_trig']
            pin_echo = settings['pin_echo']
            dus_thread = threading.Thread(target=detect_distance, args=(pin_trig, pin_echo, dus_callback ,stop_event, settings, publish_event))
            dus_thread.start()
            threads.append(dus_thread)

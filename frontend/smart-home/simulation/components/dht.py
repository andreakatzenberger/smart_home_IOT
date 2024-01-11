
from simulators.dht import run_dht_simulator
import threading
import time
from locks.print_lock import print_lock
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json
from datetime import datetime, timedelta

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5


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


def dht_callback(humidity, temperature, dht_settings, publish_event):
    global publish_data_counter, publish_data_limit
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    payload = {
         'measurement_temperature':'Temperature',
         'measurement_humidity':'Humidity',
         'simulated': dht_settings['simulated'],
         'runs_on':dht_settings['runs_on'],
         'name':dht_settings['name'],
         'value_temperature':temperature,
         'value_humidity': humidity,
        '_time': formatted_time
    }
    with print_lock:
        dht_batch.append(('dht', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def run_dht(settings, threads, stop_event, code):
        if settings['simulated']:
            dht_thread = threading.Thread(target = run_dht_simulator, args=(5, dht_callback, stop_event, settings, publish_event))
            dht_thread.start()
            threads.append(dht_thread)
        else:
            from sensors.dht import run_dht_loop, DHT
            dht = DHT(settings['pin'])
            dht_thread = threading.Thread(target=run_dht_loop, args=(dht, 5, dht_callback, stop_event, settings, publish_event))
            dht_thread.start()
            threads.append(dht_thread)

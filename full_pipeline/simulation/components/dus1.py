from simulators.dus1 import run_dus1_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dus1 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dus1_callback(distance, val, publish_event, dht_settings, code="DHTLIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Distance: {distance}m")

    temp_payload = {
        "measurement": "Distance",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": distance
    }

    with counter_lock:
        dht_batch.append(('DUS1', json.dumps(temp_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dus1(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting dus1 sumilator")
        dht1_thread = threading.Thread(target = run_dus1_simulator, args=(2, dus1_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dus1 sumilator started")
    else:
        from sensors.dht import run_dht_loop, DHT
        print("Starting dht1 loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dus1_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 loop started")

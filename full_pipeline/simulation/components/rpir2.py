from simulators.dpir1 import run_dpir1_simulator
from simulators.dht import run_dht_simulator
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
        print(f'published {publish_data_limit} rpir2 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rpir2_callback(state, publish_event, dht_settings, code="DHTLIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Motion detected")

    temp_payload = {
        "measurement": "Motion",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": "Motion detected"
    }

    with counter_lock:
        dht_batch.append(('RPIR2', json.dumps(temp_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rpir2(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting rpir2 sumilator")
        dht1_thread = threading.Thread(target = run_dpir1_simulator, args=(2, rpir2_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Rpir2 sumilator started")
    else:
        from sensors.dht import run_dht_loop, DHT
        print("Starting dht1 loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, rpir2_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 loop started")

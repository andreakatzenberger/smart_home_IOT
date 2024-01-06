from simulators.dl import run_dl_simulator
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
        print(f'published {publish_data_limit} dl values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dl_callback(state, publish_event, dht_settings, code="DHTLIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit
    global val
    if state==1:
        val="On"
    else:
        val="Off"

    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Light: {val}")

    temp_payload = {
        "measurement": "Light",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": val
    }

    with counter_lock:
        dht_batch.append(('DL', json.dumps(temp_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dl(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting dl sumilator")
        dht1_thread = threading.Thread(target = run_dl_simulator, args=(2, dl_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dl sumilator started")
    else:
        from sensors.dht import run_dht_loop, DHT
        print("Starting dl loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 loop started")

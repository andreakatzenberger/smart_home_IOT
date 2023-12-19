import threading
import time
from simulators.DUS1 import run_dus1_simulator
from sensors.DUS1 import DUS1
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dus values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dus1_callback(distance, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n\n" + "=" * 10 + " DUS1 " + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Distance: {distance}")

    payload = {
            'measurement': 'Distance',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': distance
    }
    with counter_lock:
        dht_batch.append(('dus', json.dumps(payload), 0, True))
        publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()
    

def run_dus1(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting DUS1 sumilator")
        dus1_thread = threading.Thread(target=run_dus1_simulator, args=(delay, dus1_callback, stop_event, print_lock, settings, publish_event))
        dus1_thread.start()
        threads.append(dus1_thread)
        print("DUS1 sumilator started")
    else:
        print("Starting DUS1 loop")
        dus1 = DUS1(settings['trig_pin'], settings['echo_pin'])
        dus1_thread = threading.Thread(target=run_dus1_loop, args=(dus1, delay, dus1_callback, stop_event, print_lock, settings, publish_event))
        dus1_thread.start()
        threads.append(dus1_thread)
        print("DUS1 loop started")

import time
import threading
from simulators.DL import run_dl_simulator, DL_sim
from sensors.DL import run_dl_loop, DL
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
        print(f'published {publish_data_limit} dl values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dl_callback(state, settings, publish_event):
    global publish_data_counter, publish_data_limit
    global val
    t = time.localtime()
    print("\n\n" + "=" * 10 + " DL " + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Light: {state}")

    if state=="ON":
        val=True
    else:
        val=False


    payload = {
            'measurement': 'Motion',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': val,
        }
    
    with counter_lock:
        dht_batch.append(('dl', json.dumps(payload), 0, True))
        publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dl(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting DL simualtor")
        dl = DL_sim()
        dl_thread = threading.Thread(target=run_dl_simulator, args=(dl, delay, dl_callback, stop_event, print_lock, settings, publish_event))
        dl_thread.start()
        threads.append(dl_thread)
        print("DL simualtor started")
    else:
        print("Starting DL loop")
        dl = DL(settings['pin'])
        dl_thread = threading.Thread(target=run_dl_loop, args=(dl, delay, dl_callback, stop_event, print_lock, settings, publish_event))
        dl_thread.start()
        threads.append(dl_thread)
        print("DL loop started")

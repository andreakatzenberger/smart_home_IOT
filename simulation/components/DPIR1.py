import datetime
import time
from simulators.PIR import run_pir_simulator
from sensors.PIR import PIR, run_pir_loop
import threading
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
        print(f'published {publish_data_limit} dpir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def pir_callback(state, settings, publish_event, code="PIR_OK"):
    global publish_data_counter, publish_data_limit
    if state==1:
        t = time.localtime()
        print("\n\n" + "=" * 10 + "DPIR1" + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Motion detected")


        payload = {
            'measurement': 'Motion',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': 1,
        }
        
        with counter_lock:
            dht_batch.append(('dpir', json.dumps(payload), 0, True))
            publish_data_counter += 1
        if publish_data_counter >= publish_data_limit:
            publish_event.set()



def run_dpir1(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting DPIR1 simualtor")
        dpir1_thread = threading.Thread(target=run_pir_simulator,
                                        args=(delay, pir_callback, stop_event, print_lock, settings, publish_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 simualtor started")
    else:
        print("Starting DPIR1 loop")
        dpir1 = PIR(settings['pin'])
        dpir1_thread = threading.Thread(target=run_pir_loop,
                                        args=(dpir1, delay, pir_callback, stop_event, print_lock, settings, publish_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 loop started")

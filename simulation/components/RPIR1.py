from simulators.PIR import run_pir_simulator
from sensors.PIR import PIR, run_pir_loop
import threading
import time
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
        print(f'published {publish_data_limit} rpir1 values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def pir_callback(state, settings, publish_event):
    global publish_data_counter, publish_data_limit
    t = time.localtime()
    print("\n\n" + "=" * 10 + "RPIR1" + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if state == 1:
        print(f"Motion detected")
    elif state == 0:
        print(f"Motion not detected")

    payload = {
            'measurement': 'Motion',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': 1,
        }
        
    with counter_lock:
        dht_batch.append(('rpir1', json.dumps(payload), 0, True))
        publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rpir1(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting RPIR1 simualtor")
        rpir1_thread = threading.Thread(target=run_pir_simulator,
                                        args=(delay, pir_callback, stop_event, print_lock, settings, publish_event))
        rpir1_thread.start()
        threads.append(rpir1_thread)
        print("RPIR1 simualtor started")
    else:
        print("Starting RPIR1 loop")
        rpir1 = PIR(settings['pin'])
        rpir1_thread = threading.Thread(target=run_pir_loop,
                                        args=(rpir1, delay, pir_callback, stop_event, print_lock, settings, publish_event))
        rpir1_thread.start()
        threads.append(rpir1_thread)
        print("RPIR1 loop started")

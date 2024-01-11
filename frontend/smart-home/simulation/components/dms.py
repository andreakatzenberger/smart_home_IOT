
import threading
import time
from locks.print_lock import print_lock
from simulators.dms import run_dms_simulator
from datetime import datetime, timedelta

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



def dms_callback(result, settings, publish_event):
    global publish_data_counter, publish_data_limit
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    payload = {
            'measurement': 'Membrane',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': result,
            '_time': formatted_time
    }
    # publish.single('dms-entered-pin', json.dumps({'pin': result}), hostname=HOSTNAME, port=PORT)

    with print_lock:
        dht_batch.append(('dms', json.dumps(payload), 0, True))
        publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_dms(settings, threads, stop_event):
        if settings['simulated']:
            dms_thread = threading.Thread(target = run_dms_simulator, args=(5, dms_callback, stop_event, settings, publish_event))
            dms_thread.start()
            threads.append(dms_thread)
        else:
            from sensors.dms import detect_motion
            r1 = settings['R1']
            r2 = settings['R2']
            r3 = settings['R3']
            r4 = settings['R4']
            c1 = settings['C1']
            c2 = settings['C2']
            c3 = settings['C3']
            c4 = settings['C4']
            pir_thread = threading.Thread(target=detect_motion, args=(r1, r2, r3, r4, c1, c2, c3, c4, dms_callback, stop_event, settings, publish_event))
            pir_thread.start()
            threads.append(pir_thread)

import threading
import time
from locks.print_lock import print_lock
from datetime import datetime, timedelta

from simulators.gsg import run_gsg_simulator
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json
dht_batch = []
publish_data_counter = 0
publish_data_limit = 3


def publisher_task(event, gsc_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with print_lock:
            local_gsc_batch = gsc_batch.copy()
            publish_data_counter = 0
            gsc_batch.clear()
        publish.multiple(local_gsc_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


def gsg_callback(data, settings, publish_event):

    global publish_data_counter, publish_data_limit
    accelerator_data = data[0]
    gyroscope_data = data[1]
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    for a, g in zip(accelerator_data, gyroscope_data):
        a_suspicions = False
        g_suspicious = False
        if abs(a) > 1.9:
            a_suspicions = True
        if abs(g) > 240:
            g_suspicious  = True
            
        payload = {
            'measurement': 'Gyroscope',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': round(g, 2),
            '_time': formatted_time,
            'suspicious': g_suspicious
        }
        payloadAccel = {
            'measurement': 'Accelerator',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': round(a, 2),
            '_time': formatted_time,
            'suspicious': a_suspicions

        }
        with print_lock:
            dht_batch.append(('gsg', json.dumps(payload), 0, True))
            dht_batch.append(('gsg', json.dumps(payloadAccel), 0, True))
            publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_gsg(settings, threads, stop_event):
        if settings['simulated']:
            gsc_thread = threading.Thread(target=run_gsg_simulator,
                                          args=(10, gsg_callback, stop_event, settings, publish_event))
            gsc_thread.start()
            threads.append(gsc_thread)
        else:
            from sensors.gsg import run_gsg
            # sda = settings['SDA']
            # scl = settings['SCL']
            delay = 10
            dpir_thread = threading.Thread(target=run_gsg,
                                          args=(gsg_callback, stop_event, settings, publish_event, delay))
            dpir_thread.start()
            threads.append(dpir_thread)

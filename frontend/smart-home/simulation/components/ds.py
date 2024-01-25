
from simulators.ds import run_ds_simulator
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
button_pressed_time = None
button_pressed_5_seconds = None
past_value = False

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


def ds_callback(current_value, settings, publish_event, system_event):
    global publish_data_counter, publish_data_limit, button_pressed_time, past_value, button_pressed_5_seconds


    if current_value is True:
        if system_event.is_set():
            publish.single('alarm-on-server', json.dumps({'':''}), hostname=HOSTNAME, port=PORT)
        value = 1
        if past_value == False:
            button_pressed_time = time.time()
            past_value = True
    else:
        value = 0
        if past_value == True:
            button_pressed_time = None
            past_value = False
            if button_pressed_5_seconds:
                button_pressed_5_seconds = False

    if button_pressed_time is not None and (time.time() - button_pressed_time) > 5 and not button_pressed_5_seconds :
        button_pressed_5_seconds = True

    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()
    payload = {
        'measurement': 'Pressed',
        'simulated': settings['simulated'],
        'runs_on': settings['runs_on'],
        'name': settings['name'],
        'value': value,
        '_time': formatted_time,
        'alarm':button_pressed_5_seconds
    }
    with print_lock:
        dht_batch.append(('ds', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_ds(settings, threads, stop_event, code, system_event):
        if settings['simulated']:
            ds_thread = threading.Thread(target = run_ds_simulator, args=(1, ds_callback, stop_event, settings, publish_event, system_event))
            ds_thread.start()
            threads.append(ds_thread)
        else:
            from sensors.ds import press_button
            pin = settings['pin']
            ds_thread = threading.Thread(target=press_button,
                                          args=(pin, ds_callback, stop_event, settings, publish_event, system_event))
            ds_thread.start()
            threads.append(ds_thread)

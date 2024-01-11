
import threading
import time
from locks.print_lock import print_lock
from simulators.lcd import run_lcd_simulator
from datetime import datetime, timedelta

import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

import json
dht_batch = []
publish_data_counter = 0
publish_data_limit = 5

def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with print_lock:
            local_pir_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} lcd values')
        event.clear()



def lcd_callback(result, settings, publish_event):
    global publish_data_counter, publish_data_limit
    current_datetime = datetime.now()

    adjusted_datetime = current_datetime - timedelta(hours=1)

    formatted_time = adjusted_datetime.isoformat()

    payload = {
            'measurement': 'Text',
            'simulated': settings['simulated'],
            'runs_on': settings['runs_on'],
            'name': settings['name'],
            'value': result,
            '_time': formatted_time
    }
    with print_lock:
        dht_batch.append(('lcd', json.dumps(payload), 0, True))
        publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_lcd(settings, threads, stop_event, msg):
        if settings['simulated']:
            lcd_thread = threading.Thread(target = run_lcd_simulator, args=(6, lcd_callback, stop_event, settings, publish_event, msg))
            lcd_thread.start()
            threads.append(lcd_thread)
        else:
            from sensors.lcd.LCD1602 import run_lcd_loop
            sda = settings['SDA']
            scl = settings['SCL']

            pir_thread = threading.Thread(target=run_lcd_loop, args=(lcd_callback, stop_event, settings, publish_event, msg))
            pir_thread.start()
            threads.append(pir_thread)

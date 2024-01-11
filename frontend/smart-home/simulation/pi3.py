
import threading
from settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.bir import run_bir
import time
from components.db import run_db
from components.rgb import run_rgb
from locks.print_lock import print_lock
from components.b4sd import run_b4sd
import paho.mqtt.client as mqtt
import json

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


# def run_dht_threads(settings, threads, stop_event):
#     rdht4_settings = settings['RDHT4']
#     run_dht(rdht4_settings, threads, stop_event, 'RDHT4')

def run_pir_threads(settings, threads, stop_event):
    rpir4_settings = settings['RPIR4']
    run_pir(rpir4_settings, threads, stop_event)

# def run_bir_threads(settings, threads, stop_event):
#     bir_settings = settings['BIR']

#     run_bir(bir_settings, threads, stop_event)

def run_bb_threads(settings, threads, stop_event, clock_event, alarm_event):
    db_settings = settings["BB"]
    run_db(db_settings, threads, stop_event, "BB", clock_event, alarm_event)


def run_b4sd_threads(settings, threads, stop_event, clock_event):
    bir_settings = settings['B4SD']

    run_b4sd(bir_settings, threads, stop_event, clock_event)

# def run_rgb_threads(settings, threads, stop_event, button_pressed):
#     db_settings = settings["BRGB"]
#     run_rgb(db_settings, threads, stop_event, button_pressed)

settings = load_settings('settingspi3.json')
threads = []
stop_event = threading.Event()
alarm_event = threading.Event()
clock_event = threading.Event()

def handle_message(topic, data):
    if topic == 'clock-activate':
        clock_event.set()
    elif topic == 'clock-stop':
        clock_event.clear()
    elif topic == 'alarm-on':
        print("alarm on PI3")
        alarm_event.set()
    elif topic == 'alarm-off':
        print("alarm off PI3")
        alarm_event.clear()
    # elif topic == 'bir-button-pressed':
    #     run_rgb_threads(settings, threads, stop_event, data['button'])
def on_message(client, userdata, msg):
    handle_message(msg.topic, json.loads(msg.payload.decode('utf-8')))

if __name__ == "__main__":
    # MQTT Configuration
    
    pause_event = threading.Event()
    mqtt_client = mqtt.Client()


    def on_connect(client, userdata, flags, rc):

        client.subscribe("clock-activate", qos=1)
        client.subscribe("clock-stop", qos=1)
        client.subscribe("alarm-on", qos=1)
        client.subscribe("alarm-off", qos=1)
        client.subscribe("bir-button-pressed", qos=1)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()
    print('Starting app')

    try:
        # run_dht_threads(settings, threads, stop_event)
        run_pir_threads(settings, threads, stop_event)
        # run_bir_threads(settings, threads, stop_event)
        run_b4sd_threads(settings, threads, stop_event, clock_event)

        run_bb_threads(settings, threads, stop_event, clock_event, alarm_event)
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()


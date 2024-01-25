
import threading
from settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.dus import run_dus
import time
from components.dpir import run_dpir
from components.ds import run_ds
from components.dms import run_dms
from components.dl import run_dl
from components.db import run_db
from components.gsg import run_gsg
import paho.mqtt.client as mqtt
from locks.print_lock import print_lock

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

system_event = threading.Event()


def run_pir_threads(settings, threads, stop_event):
    rpir3_settings = settings['RPIR3']

    run_pir(rpir3_settings, threads, stop_event)

def run_dpir_threads(settings, threads, stop_event):
    dpir2_settings = settings['DPIR2']

    run_pir(dpir2_settings, threads, stop_event)

def run_dus_threads(settings, threads, stop_event):
    dus2_settings = settings['DUS2']
    run_dus(dus2_settings, threads, stop_event)

def run_gsc_threads(settings, threads, stop_event):
    db_settings = settings["GSG"]
    run_gsg(db_settings, threads, stop_event)


#def on_message(client, userdata, msg):
    #handle_message(msg.topic, json.loads(msg.payload.decode('utf-8')))


if __name__ == "__main__":
    # MQTT Configuration
    settings = load_settings('settingspi2.json')
    threads = []
    stop_event = threading.Event()
    pause_event = threading.Event()
    mqtt_client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        client.subscribe("dht-lcd-display", qos=1)
        client.subscribe("system-on", qos=1)
        client.subscribe("system-off", qos=1)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()

    print('Starting app')

    try:
        run_pir_threads(settings, threads, stop_event)
        run_dpir_threads(settings, threads, stop_event)
        run_dus_threads(settings, threads, stop_event)
        run_gsc_threads(settings, threads,  stop_event)

        while True:
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()

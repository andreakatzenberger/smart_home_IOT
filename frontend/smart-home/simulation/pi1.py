
import threading
from settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.dus import run_dus
import time
from components.ds import run_ds
from components.dms import run_dms
from components.dl import run_dl
from components.db import run_db
from locks.print_lock import print_lock
import paho.mqtt.client as mqtt
import json
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


# def run_dht_threads(settings, threads, stop_event):
#     rdht1_settings = settings['RDHT1']
#     rdht2_settings = settings['RDHT2']
#     run_dht(rdht1_settings, threads, stop_event, 'RDHT1')
#     run_dht(rdht2_settings, threads, stop_event, 'RDHT2')

def run_pir_threads(settings, threads, stop_event):
    rpir1_settings = settings['RPIR1']
    rpir2_settings = settings['RPIR2']
    run_pir(rpir1_settings, threads, stop_event)
    run_pir(rpir2_settings, threads, stop_event)

def run_dpir_threads(settings, threads, stop_event):
    dpir1_settings = settings['DPIR1']

    run_pir(dpir1_settings, threads, stop_event)

# def run_ds_threads(settings, threads, stop_event, system_event):
#     ds1_settings = settings['DS1']
#     run_ds(ds1_settings, threads, stop_event, 'DS1', system_event)

def run_dus_threads(settings, threads, stop_event):
    dus1_settings = settings['DUS1']
    run_dus(dus1_settings, threads, stop_event)

# def run_dms_threads(settings, threads, stop_event):
#     dms_settings = settings['DMS']
#     run_dms(dms_settings, threads, stop_event)

def run_dl_threads(settings, threads, stop_event):
    dl_settings = settings["DL"]
    run_dl(dl_settings, threads, stop_event, "DL")

def run_db_threads(settings, threads, stop_event, clock_event, alarm_event):
    db_settings = settings["DB"]
    run_db(db_settings, threads, stop_event, "DB", clock_event, alarm_event)



def menu(stop_event):
    while not stop_event.is_set():
        user_input = input("Press 'm' to open the menu: ")
        print("user input: ", user_input)
        if user_input == "m":
            while True:
                with print_lock:
                    print("Menu Options:")
                    print("Press l to control Door Light")
                    print("Press b to control Door Buzzer")
                    print("Press 'e' to exit the menu")
                    user_input = input("Enter your choice: ")
                    if user_input == "l":
                        run_dl_threads(settings, threads, stop_event)
                        time.sleep(1)
                    elif user_input == "b":
                        run_db_threads(settings, threads, stop_event)
                        time.sleep(1)
                    elif user_input == "e":
                        print("Exiting the menu. Printing is resumed.")
                        break
        else:
            pass
def run_menu_thread(threads, stop_event):
    thread = threading.Thread(target = menu, args=(stop_event,))
    thread.start()
    threads.append(thread)

alarm_event = threading.Event()
clock_event = threading.Event()
system_event = threading.Event()
def handle_message(topic, data):
    if topic == 'dpir1-light-on':
         run_dl_threads(settings, threads, stop_event)
    elif topic == 'clock-activate':
        clock_event.set()
    elif topic == 'clock-stop':
        clock_event.clear()
    elif topic == 'alarm-on':
        print("alarm on PI1")
        alarm_event.set()
    elif topic == 'alarm-off':
        print("alarm off PI1")
        alarm_event.clear()
    elif topic == 'system-on':
        system_event.set()
    elif topic == 'system-off':
        system_event.clear()

if __name__ == "__main__":
    # MQTT Configuration
    settings = load_settings('settingspi1.json')
    threads = []
    stop_event = threading.Event()
    pause_event = threading.Event()
    mqtt_client = mqtt.Client()
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()

    def on_connect(client, userdata, flags, rc):
        client.subscribe("dpir1-light-on")
        client.subscribe("clock-activate", qos=1)
        client.subscribe("clock-stop", qos=1)
        client.subscribe("alarm-on", qos=1)
        client.subscribe("alarm-off", qos=1)
        client.subscribe("system-on", qos=1)
        client.subscribe("system-off", qos=1)
        #system-on


    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: handle_message(msg.topic, json.loads(msg.payload.decode('utf-8')))

    print('Starting app')
    
    try:
        # run_dht_threads(settings, threads, stop_event)
        run_pir_threads(settings, threads, stop_event)
        run_dpir_threads(settings, threads, stop_event)
        # run_ds_threads(settings, threads, stop_event, system_event)
        run_dus_threads(settings, threads, stop_event)
        run_db_threads(settings, threads, stop_event, clock_event, alarm_event)
        # run_dms_threads(settings, threads, stop_event)
        #run_menu_thread(threads, stop_event)
        while True:
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()

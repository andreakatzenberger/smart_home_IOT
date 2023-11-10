
import threading
from settings import load_settings
from components.dht import run_dht
from components.DS1 import run_ds1
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

if __name__ == "__main__":
    print('Starting app: smart_home_iot')
    settings = load_settings() 
    threads = []
    stop_event = threading.Event() 
    print_lock = threading.Lock()
    delay = 7

    try:
        dht1_settings = settings['DHT1']
        run_dht(dht1_settings, threads, stop_event, delay, print_lock)  

        ds1_settings = settings['DS1']
        run_ds1(ds1_settings, threads, stop_event, delay, print_lock)

        while True:
            time.sleep(3)

    except KeyboardInterrupt:
        print('Stopping app: smart_home_iot')
        for t in threads:
            stop_event.set()  

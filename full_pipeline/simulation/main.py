
import threading
from settings import load_settings
from components.dht import run_dht
from components.dpir1 import run_dpir1
from components.rpir1 import run_rpir1
from components.rpir2 import run_rpir2
from components.dus1 import run_dus1
from components.dl import run_dl
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        # dht1_settings = settings['DHT1']
        # run_dht(dht1_settings, threads, stop_event)

        # dpir1_settings = settings['DPIR1']
        # run_dpir1(dpir1_settings, threads, stop_event)

        # rpir1_settings = settings['RPIR1']
        # run_rpir1(rpir1_settings, threads, stop_event)

        # rpir2_settings = settings['RPIR2']
        # run_rpir2(rpir2_settings, threads, stop_event)

        # dus1_settings = settings['DUS1']
        # run_dus1(dus1_settings, threads, stop_event)
        
        dl_settings = settings['DL']
        run_dl(dl_settings, threads, stop_event)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()

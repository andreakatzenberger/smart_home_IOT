
import threading
from settings import load_settings
from components.dht import run_dht
from components.dpir1 import run_dpir1
from components.rpir1 import run_rpir1
from components.rpir2 import run_rpir2
from components.dus1 import run_dus1
from components.dl import run_dl
from components.DS1 import run_ds1
from components.DMS import run_dms
from components.DB import run_db
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
        run_dht(dht1_settings, threads, stop_event)
        # dht1_settings = settings['DHT1']
        # run_dht(dht1_settings, threads, stop_event, delay, print_lock,"1")
        # dht2_settings = settings['DHT2']
        # run_dht(dht2_settings, threads, stop_event, delay, print_lock, "2")
        ds1_settings = settings['DS1']
        run_ds1(ds1_settings, threads, stop_event, delay, print_lock)
        db_settings = settings['DB']
        run_db(db_settings, threads, stop_event, delay, print_lock)
        dms_settings = settings['DMS']
        run_dms(dms_settings, threads, stop_event, print_lock)


        dpir1_settings = settings['DPIR1']
        run_dpir1(dpir1_settings, threads, stop_event)

        rpir1_settings = settings['RPIR1']
        run_rpir1(rpir1_settings, threads, stop_event)

        rpir2_settings = settings['RPIR2']
        run_rpir2(rpir2_settings, threads, stop_event)
        
        dus1_settings = settings['DUS1']
        run_dus1(dus1_settings, threads, stop_event)
        
        dl_settings = settings['DL']
        run_dl(dl_settings, threads, stop_event)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
            
            # GPIO.cleanup()

# from(bucket: "example_db")
#     |> range(start: -10m)
#     |> filter(fn: (r) => r._measurement == "Humidity")

# from(bucket: "example_db")
#     |> range(start: -10m)
#     |> filter(fn: (r) => r._measurement == "Temperature")

# from(bucket: "example_db")
#     |> range(start: -10m)
#     |> filter(fn: (r) => r._measurement == "Distance")

# from(bucket: "example_db")
#     |> range(start: -10m)
#     |> filter(fn: (r) => r._measurement == "Motion")
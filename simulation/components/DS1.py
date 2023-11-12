from simulators.DS1 import run_ds1_simulator, DS1_sim
from sensors.DS1 import run_ds1_loop, DS1
from components.DB import DB
import threading
import time

def ds1_callback(state):
    t = time.localtime()
    print("\n\n" + "="*10 + " DS1 " + "="*10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Door state: {state}")

def run_ds1(settings, db_settings, threads, stop_event, delay, print_lock):
        db = DB(db_settings['simulated'], db_settings['pin'])
        if settings['simulated']:
            print("Starting DS1 simualtor")
            ds1 = DS1_sim()
            ds1_thread = threading.Thread(target = run_ds1_simulator, args=(ds1, db, delay, ds1_callback, stop_event, print_lock))
            ds1_thread.start()
            threads.append(ds1_thread)
            print("DS1 simualtor started")
        else:
            print("Starting DS1 loop")
            ds1 = DS1(settings['pin'])
            ds1_thread = threading.Thread(target=run_ds1_loop, args=(ds1, db, delay, ds1_callback, stop_event, print_lock))
            ds1_thread.start()
            threads.append(ds1_thread)
            print("DS1 loop started")
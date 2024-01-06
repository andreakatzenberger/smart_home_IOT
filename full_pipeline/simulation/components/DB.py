import time
import threading
from simulators.DB import DB_sim, run_db_simulator
from sensors.DB import  DB, run_db_loop


def db_callback(state):
    t = time.localtime()
    print("\n\n" + "=" * 10 + " DB " + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Buzzer: {state}")


def run_db(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting DB simualtor")
        db = DB_sim()
        db_thread = threading.Thread(target=run_db_simulator, args=(db, db_callback, stop_event, print_lock))
        db_thread.start()
        threads.append(db_thread)
        print("DB simualtor started")
    else:
        print("Starting DB loop")
        db = DB(settings['pin'])
        db_thread = threading.Thread(target=run_db_loop, args=(db, delay, db_callback, stop_event, print_lock))
        db_thread.start()
        threads.append(db_thread)
        print("DB loop started")
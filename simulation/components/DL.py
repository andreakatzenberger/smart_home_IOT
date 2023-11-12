import time
import threading
from simulators.DL import run_dl_simulator, DL_sim
from sensors.DL import run_dl_loop, DL


def dl_callback(state):
    t = time.localtime()
    print("\n\n" + "=" * 10 + " DL " + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Light: {state}")


def run_dl(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting DL simualtor")
        dl = DL_sim()
        dl_thread = threading.Thread(target=run_dl_simulator, args=(dl, delay, dl_callback, stop_event, print_lock))
        dl_thread.start()
        threads.append(dl_thread)
        print("DL simualtor started")
    else:
        print("Starting DL loop")
        dl = DS1(settings['pin'])
        dl_thread = threading.Thread(target=run_dl_loop, args=(dl, delay, dl_callback, stop_event, print_lock))
        dl_thread.start()
        threads.append(dl_thread)
        print("DL loop started")

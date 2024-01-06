from simulators.DMS import run_dms_simulator
from sensors.DMS import DMS, run_dms_loop
import threading
import time

def dms_callback(key):
    print(key)


def run_dms(settings, threads, stop_event, print_lock):

        if settings['simulated']:
            print("Starting DMS simualtor")
            dms_thread = threading.Thread(target = run_dms_simulator, args=( dms_callback, stop_event, print_lock))
            dms_thread.start()
            threads.append(dms_thread)
            print("DMS simulator started")
        else:
            print("Starting DMS loop")
            dms = DMS(settings['R1'],
                      settings['R2'],
                      settings['R3'],
                      settings['R4'],
                      settings['C1'],
                      settings['C2'],
                      settings['C3'],
                      settings['C4'])
            dms_thread = threading.Thread(target=run_dms_loop, args=(dms, dms_callback, stop_event, print_lock))
            dms_thread.start()
            threads.append(dms_thread)
            print("DMS loop started")
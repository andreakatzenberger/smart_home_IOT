from simulators.PIR import run_pir_simulator
from sensors.PIR import PIR, run_pir_loop
import threading
import time


def pir_callback(state):
    t = time.localtime()
    print("\n\n" + "=" * 10 + "DPIR1" + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if state == 1:
        print(f"Motion detected")
    elif state == 0:
        print(f"Motion not detected")


def run_dpir1(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting DPIR1 simualtor")
        dpir1_thread = threading.Thread(target=run_pir_simulator,
                                        args=(delay, pir_callback, stop_event, print_lock))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 simualtor started")
    else:
        print("Starting DPIR1 loop")
        dpir1 = PIR(settings['pin'])
        dpir1_thread = threading.Thread(target=run_pir_loop,
                                        args=(dpir1, delay, pir_callback, stop_event, print_lock))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 loop started")

from simulators.PIR import run_pir_simulator
from sensors.PIR import DPIR1
import threading
import time


def dpir1_callback(state):
    t = time.localtime()
    print("\n\n" + "=" * 10 + "DPIR1" + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if state == 1:
        print(f"Motion detected\n")
    elif state == 0:
        print(f"Motion not detected\n")


def run_dpir1(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting DPIR1 sumilator")
        dpir1_thread = threading.Thread(target=run_pir_simulator,
                                        args=(delay, dpir1_callback, stop_event, print_lock))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 sumilator started")
    else:
        print("Starting DPIR1 loop")
        # dpir1 = DPIR1(settings['pin'])
        # dpir1_thread = threading.Thread(target=run_dpir1_loop,
        #                                 args=(dpir1, delay, dpir1_callback, stop_event, print_lock))
        # dpir1_thread.start()
        # threads.append(dpir1_thread)
        # print("DPIR1 loop started")

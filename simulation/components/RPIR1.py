from simulators.PIR import run_pir_simulator
from sensors.PIR import DPIR1
import threading
import time


def rpir1_callback(state):
    t = time.localtime()
    print("\n\n" + "=" * 10 + "RPIR1" + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if state == 1:
        print(f"Motion detected\n")
    elif state == 0:
        print(f"Motion not detected\n")


def run_rpir1(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting RPIR1 sumilator")
        rpir1_thread = threading.Thread(target=run_pir_simulator,
                                        args=(delay, rpir1_callback, stop_event, print_lock))
        rpir1_thread.start()
        threads.append(rpir1_thread)
        print("RPIR1 sumilator started")
    else:
        print("Starting RPIR1 loop")
        # rpir1 = DPIR1(settings['pin'])
        # rpir1_thread = threading.Thread(target=run_rpir1_loop,
        #                                 args=(rpir1, delay, rpir1_callback, stop_event, print_lock))
        # rpir1_thread.start()
        # threads.append(rpir1_thread)
        # print("RPIR1 loop started")

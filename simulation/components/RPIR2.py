from simulators.PIR import run_pir_simulator
from sensors.PIR import PIR, run_pir_loop
import threading
import time


def pir_callback(state):
    t = time.localtime()
    print("\n\n" + "=" * 10 + "RPIR2" + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if state == 1:
        print(f"Motion detected\n")
    elif state == 0:
        print(f"Motion not detected\n")


def run_rpir2(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting RPIR2 simualtor")
        rpir2_thread = threading.Thread(target=run_pir_simulator,
                                        args=(delay, pir_callback, stop_event, print_lock))
        rpir2_thread.start()
        threads.append(rpir2_thread)
        print("RPIR2 simualtor started")
    else:
        print("Starting RPIR2 loop")
        rpir2 = PIR(settings['pin'])
        rpir2_thread = threading.Thread(target=run_pir_loop,
                                        args=(rpir2, delay, pir_callback, stop_event, print_lock))
        rpir2_thread.start()
        threads.append(rpir2_thread)
        print("RPIR2 loop started")

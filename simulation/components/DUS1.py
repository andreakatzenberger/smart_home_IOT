import threading
import time
from simulators.DUS1 import run_dus1_simulator
# from sensors.DUS1 import DUS1

def dus1_callback(distance):
    t = time.localtime()
    print("\n\n" + "="*10 + " DUS1 " + "="*10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Distance: {distance}")

def run_dus1(settings, threads, stop_event, delay, print_lock):
    if settings['simulated']:
        print("Starting DUS1 sumilator")
        dus1_thread = threading.Thread(target=run_dus1_simulator, args=(delay, dus1_callback, stop_event, print_lock))
        dus1_thread.start()
        threads.append(dus1_thread)
        print("DUS1 sumilator started")
    else:
        print("Starting rdht1 loop")
        # dht = DHT(settings['pin'])
        # dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, delay, uds_callback, stop_event))
        # dht1_thread.start()
        # threads.append(dht1_thread)
        # print("DUS1 loop started")
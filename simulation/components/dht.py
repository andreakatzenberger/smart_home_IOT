from simulators.dht import run_dht_simulator
from sensors.dht import run_dht_loop, DHT
import threading
import time

def dht_callback(humidity, temperature, code):
    t = time.localtime()
    print("\n\n" + "="*10 + " DHT1 " + "="*10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event, delay, print_lock):

        if settings['simulated']:
            print("Starting dht1 sumilator")
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(delay, dht_callback, stop_event, print_lock))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht1 sumilator started")
        else:
            print("Starting dht1 loop")
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, delay, dht_callback, stop_event, print_lock))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht1 loop started")

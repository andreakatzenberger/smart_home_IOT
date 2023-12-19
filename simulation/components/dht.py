from simulators.dht import run_dht_simulator
from sensors.dht import run_dht_loop, DHT
import threading
import time

def dht_callback(humidity, temperature, code, id):
    t = time.localtime()
    print("\n\n" + "="*10 + " DHT"+id+" " + "="*10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event, delay, print_lock, id):

        if settings['simulated']:
            print(f"Starting DHT{id} simualtor")
            dht_thread = threading.Thread(target = run_dht_simulator, args=(delay, dht_callback, stop_event, print_lock, id))
            dht_thread.start()
            threads.append(dht_thread)
            print(f"DHT{id} simualtor started")
        else:
            print(f"Starting DHT{id} loop")
            dht = DHT(settings['pin'])
            dht_thread = threading.Thread(target=run_dht_loop, args=(dht, delay, dht_callback, stop_event, print_lock, id))
            dht_thread.start()
            threads.append(dht_thread)
            print(f"DHT{id} loop started")

import time
import random


def generate_value():
    while True:
        accelerator_data = [round(random.uniform(-2, 2), 3) for i in range(3)]
        gyro_data = [round(random.uniform(-250, 250), 3) for i in range(3)]

        yield [accelerator_data, gyro_data]


def run_gsg_simulator(delay, callback, stop_event, settings, publish_event):
    for data in generate_value():
        time.sleep(delay)  # Delay between readings (adjust as needed)
        callback(data, settings, publish_event)
        if stop_event.is_set():
            break

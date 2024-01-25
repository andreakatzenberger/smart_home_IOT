#!/usr/bin/env python3
from gyro.MPU6050 import MPU6050
import time

mpu = MPU6050.MPU6050()  # instantiate a MPU6050 class object
accelerator = [0] * 3  # store accelerometer data
gyroscope = [0] * 3  # store gyroscope data
def setup():
    mpu.dmp_initialize()  # initialize MPU6050


def loop(callback, stop_event, settings, publish_event, delay):
    while True:
        if stop_event.is_set():
            break
        accelerator = mpu.get_acceleration()  # get accelerometer data
        gyroscope = mpu.get_rotation()  # get gyroscope data

        accelerator_values = [accelerator[0]/ 16384.0, accelerator[1]/ 16384.0, accelerator[2]/ 16384.0]
        gyroscope_values = [gyroscope[0]/ 131.0, gyroscope[1]/ 131.0, gyroscope[2]/ 131.0]


        callback(settings, publish_event, gyroscope_values, accelerator_values)
        time.sleep(delay)


def run_gsg(callback, stop_event, settings, publish_event, delay): 
    setup()
    try:
        loop(callback, stop_event, settings, publish_event, delay)
    except KeyboardInterrupt:
        pass
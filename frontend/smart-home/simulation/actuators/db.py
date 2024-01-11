try:
    import RPi.GPIO as GPIO
except:
    print('Cant load')
import time
from locks.print_lock import print_lock2

def buzz(pin, callback, stop_event, settings, publish_event, clock_event, alarm_event):
    pin = int(pin)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    while True:
        if stop_event.is_set():
            break
        pitch = 440
        duration = 0.1
        period = 1.0 / pitch
        cycles = int(duration * pitch)
        is_bb = clock_event.is_set() and settings['name'] == 'BB'
        if is_bb or alarm_event.is_set():
            for i in range(cycles):
                GPIO.output(pin, True)
                time.sleep(0.01)
                GPIO.output(pin, False)
                time.sleep(0.01)
            callback(settings, publish_event)
        time.sleep(1)

try:
    import RPi.GPIO as GPIO
except:
    pass
from locks.print_lock import print_lock
import time

def motion_detected(channel,callback, settings, publish_event):
    callback(True, settings, publish_event)

def no_motion(channel):
    pass


def detect_motion(pin, callback, stop_event, settings, publish_event):
    PIR_PIN = int(pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=lambda channel: motion_detected(channel, callback, settings, publish_event))
    GPIO.add_event_detect(PIR_PIN, GPIO.FALLING, callback=no_motion)
    input("Press any key to exit...")


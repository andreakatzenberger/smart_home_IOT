try:
    import RPi.GPIO as GPIO
except:
    print('Cant load')
import time

def run_light(pin, callback, stop_event, settings, publish_event):

    pin = int(pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    callback(settings, publish_event)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(10)
    callback(settings, publish_event)
    GPIO.output(pin, GPIO.LOW)


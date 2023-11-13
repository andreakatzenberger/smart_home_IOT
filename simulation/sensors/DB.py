try:
    import RPi.GPIO as GPIO
except:
    pass
import time
import keyboard

class DB(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def buzz(self, callback, print_lock):
        keyboard.wait('B')
        GPIO.output(self.pin, GPIO.HIGH)
        with print_lock:
            callback(" DB buzzing! ")
        time.sleep(2)
        GPIO.output(self.pin, GPIO.LOW)
        


def run_db_loop(db, delay, callback, stop_event, print_lock):
    while True:
        time.sleep(delay)
        db.buzz(callback, print_lock)
        if stop_event.is_set():
            break
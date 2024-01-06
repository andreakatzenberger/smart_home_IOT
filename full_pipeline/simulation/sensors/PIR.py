import time

try:
    import RPi.GPIO as GPIO
except:
    pass


class PIR(object):
    def __init__(self, pin, initial_state=0):
        self.pin = pin
        self.state = initial_state
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=motion)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=no_motion)

    def motion(self):
        self.state = 1

    def no_motion(self):
        self.state = 0

    def read_dl(self):
        return self.state


def run_pir_loop(pir, delay, callback, stop_event, print_lock):
    while True:
        time.sleep(delay)
        state = pir.read_dl()
        with print_lock:
            callback(state)
        if stop_event.is_set():
            break

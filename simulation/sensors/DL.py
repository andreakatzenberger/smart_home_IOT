import time

try:
    import RPi.GPIO as GPIO
except:
    pass


class DL(object):
    def __init__(self, pin, initial_state=0):
        self.pin = pin
        self.state = initial_state
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def change_detected(self):
        keyboard.wait('L')
        if self.state == 0:
            self.state = 1
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            self.state = 0
            GPIO.output(self.pin, GPIO.LOW)
        return self.read_dl()

    def read_dl(self):
        return self.state


def parse_state(code):
    if code == 1:
        return "On"
    if code == 0:
        return "Off"


def run_dl_loop(dl, delay, callback, stop_event, print_lock):
    while True:
        time.sleep(delay)
        code = dl.change_detected()
        state = parse_state(code)
        with print_lock:
            callback(state)
        if stop_event.is_set():
            break

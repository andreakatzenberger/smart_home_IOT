import time

try:
    import RPi.GPIO as GPIO
except:
    pass


class DUS1:
    def __init__(self, trig_pin, echo_pin):
        self.TRIG_PIN = int(trig_pin)
        self.ECHO_PIN = int(echo_pin)
        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.TRIG_PIN, False)
        time.sleep(0.2)
        GPIO.output(self.TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(self.ECHO_PIN) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(self.ECHO_PIN) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300) / 2
        return distance


def run_dus1_loop(dus1, delay, callback, stop_event, print_lock):
    while True:
        time.sleep(delay)
        distance = dus1.get_distance()
        with print_lock:
            callback(distance)
        if stop_event.is_set():
            break

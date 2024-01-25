try:
    import RPi.GPIO as GPIO
except:
    pass
import time

def detect_distance(trig_pin, echo_pin, callback, stop_event, settings, publish_event):

    GPIO.setmode(GPIO.BCM)
    TRIG_PIN = int(trig_pin)
    ECHO_PIN = int(echo_pin)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    def get_distance():
        GPIO.output(TRIG_PIN, False)
        time.sleep(0.2)
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(ECHO_PIN) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(ECHO_PIN) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300)/2
        return distance
    while True:
            distance = get_distance()
            if distance is not None:
                callback(distance, settings, publish_event)
            time.sleep(0.5)
            if stop_event.is_set():
                break
    
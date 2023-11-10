import time
try:
	import RPi.GPIO as GPIO
except:
	pass

class DS1(object):
    def __init__(self, pin, initial_state=0):
        self.pin = pin
        self.state = initial_state
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.change_detected, bouncetime=50)

    def change_detected(self, channel):
        input_state = GPIO.input(self.pin)
        if input_state != self.state:
            self.state = input_state

    def readDS1(self):
        return self.state

def parseState(code):
	if code == 1:
		return "OPEN"
	if code == 0:
		return "CLOSED"
	
def run_ds1_loop(ds1, delay, callback, stop_event, print_lock):
		while True:
			time.sleep(delay)  # Delay between readings
			code = ds1.readDS1()
			state = parseState(code)
			with print_lock:
				callback(state)
			if stop_event.is_set():
					break

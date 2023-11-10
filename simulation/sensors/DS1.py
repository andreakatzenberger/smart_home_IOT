import time
try:
	import RPi.GPIO as GPIO
except:
	pass

class DS1(object):
	
	#state 0  = zakljucano???  ako je dugme povezano an GND i PUD_UP
	def __init__(self, pin):
		self.pin = pin
		self.state = 1

	def change_detected(self):
		input = GPIO.input(self.pin)
		if input != self.state:
			self.state = input

	def readDS1(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.change_detected, bouncetime=50)

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

try:
    import RPi.GPIO as GPIO
except:
    pass
import time

class DB(object):

    def __init__(self, simulated, pin=0):
        self.simulated = simulated
        print(f"DB created!  simulated: {self.simulated}")
        if not simulated:
            self.pin = pin
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)

    def buzz(self):
        if not self.simulated:
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(self.pin, GPIO.LOW)
            print("\n=====DB buzzing!=====\n")
        else:
            print("\n=====DB sim buzzing!=====\n")

        
import time
import random
import keyboard

class DS1_sim(object):
     
    def __init__(self, initial_state=0):
        self.inital_state = initial_state

    def read_state(self):
        return self.inital_state
    
    def wait_for_key(self):
        keyboard.wait('X')
        if self.inital_state == 0:
            self.inital_state = 1
        else:
            self.inital_state = 0
            
        return self.read_state()

def parse_state(code):
	if code == 1:
		return "OPEN"
	if code == 0:
		return "CLOSED"
	
def run_ds1_simulator(ds1, delay, callback, stop_event, print_lock):
    while True:
        code = ds1.wait_for_key()
        state = parse_state(code)
        with print_lock:
            callback(state)
        if stop_event.is_set():
            break
              
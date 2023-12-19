import time
import random
import keyboard


class DL_sim(object):

    def __init__(self, initial_state=0):
        self.inital_state = initial_state

    def read_state(self):
        return self.inital_state

    def wait_for_key(self):
        keyboard.wait('L')
        if self.inital_state == 0:
            self.inital_state = 1
        else:
            self.inital_state = 0

        return self.read_state()


def parse_state(code):
    if code == 1:
        return "ON"
    if code == 0:
        return "OFF"


def run_dl_simulator(dl, delay, callback, stop_event, print_lock, settings, publish_event):
    while True:
        code = dl.wait_for_key()
        state = parse_state(code)
        with print_lock:
            callback(state, settings, publish_event)
        if stop_event.is_set():
            break

import time
import keyboard

class DB_sim(object):

    def buzz(self, callback, print_lock):
        keyboard.wait('B')
        with print_lock:
            callback(" DB buzzing! ")
        
def run_db_simulator(db, callback, stop_event, print_lock):
    while True:
        db.buzz(callback, print_lock)
        if stop_event.is_set():
            break
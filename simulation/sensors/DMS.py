try:
    import RPi.GPIO as GPIO
except:
    pass
import time


class DMS(object):
    def __init__(self, R1, R2, R3, R4, C1, C2, C3, C4):
        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.R4 = R4
        self.C1 = C1
        self.C2 = C2
        self.C3 = C3
        self.C4 = C4

        GPIO.setup(R1, GPIO.OUT)
        GPIO.setup(R2, GPIO.OUT)
        GPIO.setup(R3, GPIO.OUT)
        GPIO.setup(R4, GPIO.OUT)

        GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def readLine(self, line, characters, callback, print_lock):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.C1) == 1):
            with print_lock:
                callback(characters[0])
        if(GPIO.input(self.C2) == 1):
            with print_lock:
                callback(characters[1])
        if(GPIO.input(self.C3) == 1):
            with print_lock:
                callback(characters[2])
        if(GPIO.input(self.C4) == 1):
            with print_lock:
                callback(characters[3])
        GPIO.output(line, GPIO.LOW)




def run_dms_loop(dms, callback, stop_event, print_lock):
    while True:
        dms.readLine(dms.R1, ["1","2","3","A"], callback, print_lock)
        dms.readLine(dms.R2, ["4","5","6","B"], callback, print_lock)
        dms.readLine(dms.R3, ["7","8","9","C"], callback, print_lock)
        dms.readLine(dms.R4, ["*","0","#","D"], callback, print_lock)
        time.sleep(0.2)

        if stop_event.is_set():
            break

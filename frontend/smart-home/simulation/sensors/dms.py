try:
    import RPi.GPIO as GPIO
except:
    pass
import time
from locks.print_lock import print_lock

def detect_motion(r1, r2, r3, r4, c1, c2, c3, c4, dms_callback, stop_event, settings, publish_event):
    R1 = int(r1)
    R2 = int(r2)
    R3 = int(r3)
    R4 = int(r4)

    C1 = int(c1)
    C2 = int(c2)
    C3 = int(c3)
    C4 = int(c4)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(R3, GPIO.OUT)
    GPIO.setup(R4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def readLine(line, characters):
        line = ''
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(C1) == 1):
            line += characters[0]
        if(GPIO.input(C2) == 1):
            line += characters[1]

        if(GPIO.input(C3) == 1):
            line += characters[2]

        if(GPIO.input(C4) == 1):
            line += characters[3]
        GPIO.output(line, GPIO.LOW)

        return line
    lines = ''

    while True:
        # call the readLine function for each row of the keypad
        lines += readLine(R1, ["1","2","3","A"])
        lines += readLine(R2, ["4","5","6","B"])
        lines += readLine(R3, ["7","8","9","C"])
        lines += readLine(R4, ["*","0","#","D"])
        # 5 bcz of #
        if len(lines) == 5:
            dms_callback(lines, settings, publish_event)
            lines = ''
        time.sleep(0.02)
        if stop_event.is_set():
            break


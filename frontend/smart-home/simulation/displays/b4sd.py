# import RPi.GPIO as GPIO
# import time
# GPIO.setmode(GPIO.BCM)
 
# # GPIO ports for the 7seg pins
# segments =  (11,4,23,8,7,10,18,25)
# # 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
 
# for segment in segments:
#     GPIO.setup(segment, GPIO.OUT)
#     GPIO.output(segment, 0)
 
# # GPIO ports for the digit 0-3 pins 
# digits = (22,27,17,24)
# # 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
 
# for digit in digits:
#     GPIO.setup(digit, GPIO.OUT)
#     GPIO.output(digit, 1)
 
# num = {' ':(0,0,0,0,0,0,0),
#     '0':(1,1,1,1,1,1,0),
#     '1':(0,1,1,0,0,0,0),
#     '2':(1,1,0,1,1,0,1),
#     '3':(1,1,1,1,0,0,1),
#     '4':(0,1,1,0,0,1,1),
#     '5':(1,0,1,1,0,1,1),
#     '6':(1,0,1,1,1,1,1),
#     '7':(1,1,1,0,0,0,0),
#     '8':(1,1,1,1,1,1,1),
#     '9':(1,1,1,1,0,1,1)}

# def run():
#     try:
#         while True:
#             n = time.ctime()[11:13]+time.ctime()[14:16]
#             s = str(n).rjust(4)
#             for digit in range(4):
#                 for loop in range(0,7):
#                     GPIO.output(segments[loop], num[s[digit]][loop])
#                     if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
#                         GPIO.output(25, 1)
#                     else:
#                         GPIO.output(25, 0)
#                 GPIO.output(digits[digit], 0)
#                 time.sleep(0.001)
#                 GPIO.output(digits[digit], 1)
#     finally:
#         GPIO.cleanup()
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# GPIO ports for the 7seg pins
segments = (11, 4, 23, 8, 7, 10, 18, 25)

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# GPIO ports for the digit 0-3 pins
digits = (22, 27, 17, 24)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num = {' ': (0, 0, 0, 0, 0, 0, 0),
       '0': (1, 1, 1, 1, 1, 1, 0),
       '1': (0, 1, 1, 0, 0, 0, 0),
       '2': (1, 1, 0, 1, 1, 0, 1),
       '3': (1, 1, 1, 1, 0, 0, 1),
       '4': (0, 1, 1, 0, 0, 1, 1),
       '5': (1, 0, 1, 1, 0, 1, 1),
       '6': (1, 0, 1, 1, 1, 1, 1),
       '7': (1, 1, 1, 0, 0, 0, 0),
       '8': (1, 1, 1, 1, 1, 1, 1),
       '9': (1, 1, 1, 1, 0, 1, 1)}

def run(callback, stop_event, settings, publish_event, clock_event):
    is_empty = False
    try:
        while True:
            if clock_event.is_set():
                if not is_empty:
                    current_time = time.strftime("%H %M")
                    is_empty = True
                else:
                    current_time = "    "
                    is_empty = False
                time.sleep(0.5)
            else:
                current_time = time.strftime("%H %M")
            for digit in range(4):
                for loop in range(0, 7):
                    GPIO.output(segments[loop], num[current_time[digit]][loop])

                # Blink the colon on even seconds
                if int(time.time()) % 2 == 0 and digit == 1:
                    GPIO.output(25, 1)
                else:
                    GPIO.output(25, 0)

                GPIO.output(digits[digit], 0)
                time.sleep(0.001)
                GPIO.output(digits[digit], 1)
                callback(str(current_time), settings, publish_event)
            if stop_event.is_set():
                break
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


try:
    import RPi.GPIO as GPIO
except:
    pass
import time
from locks.print_lock import print_lock

import RPi.GPIO as GPIO
import time

# def check_button_state(channel, callback, settings, publish_event):
#     while GPIO.input(channel) == GPIO.HIGH:  # Check if the button is still pressed
#         callback(True, settings, publish_event)
#         time.sleep(0.1)  # Adjust the sleep duration as needed for your application
#     callback(False, settings, publish_event)
#
# def press_button(pin, callback, stop_event, settings, publish_event):
#     PORT_BUTTON = int(pin)
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
#     try:
#         while True:
#             GPIO.wait_for_edge(PORT_BUTTON, GPIO.FALLING)
#             check_button_state(PORT_BUTTON, callback, settings, publish_event)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         GPIO.cleanup()
import RPi.GPIO as GPIO
import time

def check_button_state(channel, callback, settings, publish_event, system_event):
    while GPIO.input(channel) == GPIO.HIGH:  # Check if the button is still pressed
        callback(True, settings, publish_event, system_event)
        time.sleep(0.1)  # Adjust the sleep duration as needed for your application
    callback(False, settings, publish_event, system_event)

def press_button(pin, callback, stop_event, settings, publish_event, system_event):
    PORT_BUTTON = int(pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        while True:
            GPIO.wait_for_edge(PORT_BUTTON, GPIO.FALLING)
            check_button_state(PORT_BUTTON, callback, settings, publish_event, system_event)
            if stop_event.is_set():
                break
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
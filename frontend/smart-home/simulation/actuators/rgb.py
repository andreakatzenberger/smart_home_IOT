try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
except:
    print('Cant load')




def turnOff(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
def white(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
def red(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

def green(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
def blue(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
def yellow(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
def purple(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
def lightBlue(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)

def run(rgb_callback, stop_event, settings, publish_event, rr, gg, bb, button_pressed):
    GPIO.setmode(GPIO.BCM)

    RED_PIN = rr
    GREEN_PIN = gg
    BLUE_PIN = bb

    #set pins as outputs
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    try:
        #ButtonsNames = ["LEFT",   "RIGHT",      "UP",       "DOWN",     
          #"2",          "3",          "1",        "OK",        "4",         
        # "5",         "6",         "7",         "8",          "9",        "*",        
        # "0",        "#"]  # String list in same order as HEX list
        while True:
            if button_pressed == '0':
                turnOff(rr, gg, bb)
            elif button_pressed == '1':
                white(rr, gg, bb)
            elif button_pressed == '2':
                red(rr, gg, bb)
            elif button_pressed == '3':
                green(rr, gg, bb)
            elif button_pressed == '4':
                blue(rr, gg, bb)
            elif button_pressed == '5':
                lightBlue(rr, gg, bb)
            elif button_pressed == '6':
                purple(rr, gg, bb)
            elif button_pressed == '7':
                yellow(rr, gg, bb)
            rgb_callback(settings, publish_event, button_pressed)
            if stop_event.is_set():
                GPIO.cleanup()
                break
    except KeyboardInterrupt:
        GPIO.cleanup()

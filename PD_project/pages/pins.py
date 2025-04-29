import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class Pins:
    
    def __init__(self, pin1, pin2, pin3, r1, r2, enable, start):
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.r1 = r1
        self.r2 = r2
        self.enable = enable
        self.start = start
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.setup(self.pin3, GPIO.OUT)
        GPIO.setup(self.r1, GPIO.OUT)
        GPIO.setup(self.r2, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)
        GPIO.setup(self.start, GPIO.OUT)

    
    def all_pin_low(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
        GPIO.output(self.pin3, GPIO.LOW)
        GPIO.output(self.r1, GPIO.HIGH)
        GPIO.output(self.r2, GPIO.HIGH)
        GPIO.output(self.enable, GPIO.LOW)
        GPIO.output(self.start, GPIO.LOW)


    def reset_varPins(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
        GPIO.output(self.pin3, GPIO.LOW)

    def out_to_pins(self, var):
        match var:
            case 1:
                GPIO.output(self.pin1, GPIO.LOW)
                GPIO.output(self.pin2, GPIO.LOW)
                GPIO.output(self.pin3, GPIO.HIGH)
                
            case 2:
                GPIO.output(self.pin1, GPIO.LOW)
                GPIO.output(self.pin2, GPIO.HIGH)
                GPIO.output(self.pin3, GPIO.LOW)
                
            case 3:
                GPIO.output(self.pin1, GPIO.LOW)
                GPIO.output(self.pin2, GPIO.HIGH)
                GPIO.output(self.pin3, GPIO.HIGH)
                
            case 4:
                GPIO.output(self.pin1, GPIO.HIGH)
                GPIO.output(self.pin2, GPIO.LOW)
                GPIO.output(self.pin3, GPIO.LOW)
                 
            case 5:
                GPIO.output(self.pin1, GPIO.HIGH)
                GPIO.output(self.pin2, GPIO.LOW)
                GPIO.output(self.pin3, GPIO.HIGH)
    
    def relay_low(self):
        GPIO.output(self.r1, GPIO.HIGH)
        GPIO.output(self.r2, GPIO.HIGH)

    def relay_activate(self):
        GPIO.output(self.r1, GPIO.LOW) 
        GPIO.output(self.r2, GPIO.HIGH) 
        time.sleep(5)
        GPIO.output(self.r1, GPIO.HIGH) 
        GPIO.output(self.r2, GPIO.LOW) 
        time.sleep(5)
        GPIO.output(self.r1, GPIO.LOW)
        GPIO.output(self.r2, GPIO.LOW) 

    def enable_low(self):
        GPIO.output(self.enable, GPIO.LOW)
    def enable_high(self):
        GPIO.output(self.enable, GPIO.HIGH)

    def start_low(self):
        GPIO.output(self.start, GPIO.LOW)
    def start_high(self):
        GPIO.output(self.start, GPIO.HIGH)

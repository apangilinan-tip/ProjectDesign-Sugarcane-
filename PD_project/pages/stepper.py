import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class Stepper:
    
    def __init__(self, ena, dirc, pul):
        self.ena = ena
        self.dirc = dirc
        self.pul = pul
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.setup(self.dirc, GPIO.OUT)
        GPIO.setup(self.pul, GPIO.OUT)
    
    def run(self):
        while True:
            GPIO.output(self.pul, GPIO.HIGH)
            time.sleep(0.0005)
            GPIO.output(self.pul, GPIO.LOW)
            time.sleep(0.0005)

    def dir_low(self):
        GPIO.output(self.dirc, GPIO.LOW)
    
    def dir_high(self):
        GPIO.output(self.dirc, GPIO.HIGH)

    def ena_low(self):
        GPIO.output(self.ena, GPIO.LOW)
    
    def ena_high(self):
        GPIO.output(self.ena, GPIO.HIGH)


from stepper import Stepper
from gpiozero import DistanceSensor
from pins import Pins
from camera import Camera



class Components:
    def setup(self):

        #Pins(pin1, pin2, pin3, r1, r2, enable, start)
        self.pins = Pins(14,15,18,23,24,22,27)
        self.pins.all_pin_low()


        #motor pins/flags ena, dir, pul
        self.stepper = Stepper(11,9,10)
        
        #ultrasonic
        self.ultrasonic = DistanceSensor(echo=17, trigger=4)

        #camera setup
        self.cam = Camera(0)
        self.cam.start_camera()

    
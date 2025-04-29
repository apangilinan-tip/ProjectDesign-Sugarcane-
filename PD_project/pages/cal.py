import array
import sys
import time
import RPi.GPIO as GPIO
import threading

from stepper import Stepper
from gpiozero import DistanceSensor
from pins import Pins
from camera import Camera
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



try:

    #Pins(pin1, pin2, pin3, r1, r2, enable, start)
    pins = Pins(18,15,14,27,22,23,24)


    #motor pins/flags ena, dir, pul
    stepper = Stepper(11,9,10)
    
    #ultrasonic
    ultrasonic = DistanceSensor(echo=17, trigger=4)

    #camera setup
    cam = Camera(0)
    cam.start_camera()


    print("\n\nSetup Complete. Proceed?\n")
    input()  

except Exception as e:
    print(f"Setup failed. Exiting program. Error {e}")
    sys.exit()

while True:
    try:
        while True:
            print("-----------pins calibrate---------")

            ans = input("proceed? y/n\n")
            if ans == "n":
                break

            pins.all_pin_low()
            print("all pins low")
            input()

            pins.out_to_pins(1)
            print("var = 1")
            input()

            pins.out_to_pins(5)
            print("var = 5")
            input()

            pins.out_to_pins(1)
            print("var = 1")
            input()

            pins.out_to_pins(2)
            print("var = 2")
            input()
            
            pins.out_to_pins(1)
            print("var = 1")
            input()

            pins.reset_varPins()
            print("reset var")
            input()

            print("relay activate")
            pins.relay_activate()
            input()

            print("relay low")
            pins.relay_low()
            input()

            pins.enable_high()
            print("enable high")
            input()

            pins.enable_low()
            print("enable low")
            input()

            pins.start_high()
            print("start high")
            input()

            pins.start_low()
            print("start_low")
            input()

            ans = input('exit? y /n\n')

            if ans == "y":
                break

        while True:

            print("-----------stepper calibrate---------")

            ans = input("proceed? y/n\n")
            if ans == "n":
                break

            print("stepper run, ena low")
            thread = threading.Thread(target=stepper.run, daemon=True)
            thread.start()
            stepper.ena_low()
            input()

            print("stepper run, ena high")
            stepper.ena_high()
            input()

            print("stepper run, ena low,  dir low")
            stepper.dir_low()
            stepper.ena_low()
            input()

            print("stepper run, dir high")
            stepper.ena_high()
            stepper.dir_high()
            stepper.ena_low()
            input()

            print("stepper run, ena high")
            stepper.ena_high()
            input()


            ans = input('exit? y /n\n')

            if ans == "y":
                break

        while True:

            print("-----------ultrasonic---------")

            ans = input("proceed? y/n")
            if ans == "n":
                break
            for i in range(20):

                print(ultrasonic.distance)
                time.sleep(1)    

            ans = input('exit? y /n\n')

            if ans == "y":
                break

        while True:
            print("-----------camera---------")
            ans = input("proceed? y/n\n")
            if ans == "n":
                break
            cam.capture_image("test.jpg")

            ans = input('exit? y /n\n')

            if ans == "y":
                break

    except Exception as e:
        print(f"error. {e}")
        input()

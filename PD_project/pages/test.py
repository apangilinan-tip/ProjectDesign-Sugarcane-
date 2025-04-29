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

#setup
try:

    #counters counter[0]--> caneCount [6]--> waitCount
    counter = array.array('i',[0,0,0,0,0,0,0])

    #Pins(pin1, pin2, pin3, r1, r2, enable, start)
    pins = Pins(14,15,18,23,24,22,27)
    pins.all_pin_low()


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


var = 1 #temp

#----------------------------------#
#process start    
try:
     pins.start_high()
     print("Start High")
     thread = threading.Thread(target=stepper.run, daemon=True)
     thread.start()
     stepper.ena_low()
     print("conveyor initiated")
     pins.relay_activate()
     print("cane release")

     while True:
          

          #detect cane within range of camera
          dist = ultrasonic.distance 
          if dist < 1.0:
               print("Ultrasonic in range: " + str(dist))
               counter[0]+=1 #cane count
               name= str(counter[0])+"_cane.jpg"
               cam.capture_image("images/"+name)
               print("Image captured")

               #enaPin disable
               pins.enable_low()
               print("ena: LOW")
               pins.reset_varPins()
               print("reset varpin")


               #temp ML var detection
               if var == 5:
                    var = 1
               else:
                    var += 1
          
               print("Variety: "+str(var))
               #varPins activate, increment varCount

               counter[var]+=1
               pins.out_to_pins(var)
               print("var: sent")
               #enaPin enable
               pins.enable_high()
               print("ena: HIGH")

               print("cane #"+str(counter[0])+" Variety:"+str(var)+
                    "\nVariety 1:"+str(counter[1])+
                    "\nVariety 2:"+str(counter[2])+
                    "\nVariety 3:"+str(counter[3])+
                    "\nVariety 4:"+str(counter[4])+
                    "\nVariety 5:"+str(counter[5]))
               
               time.sleep(3)#sync with arduino
               input()#temp
               pins.relay_activate()
               print("cane release")
               counter[6] = 0
          else:
               counter[6] += 1 #wait counter
               if counter[6]==5:
                    pins.relay_activate()
                    print("additional cane released")
               print("Ultrasonic not in range. Count: "+str(counter[6]))
               time.sleep(2)
          
          if counter[6] >= 10:
               pins.start_low()
               print("Start = 0")
               print("No Cane Detected.\nSUMMARY\nTotal Cane: "+str(counter[0])+
                    "\nVariety 1:"+str(counter[1])+
                    "\nVariety 2:"+str(counter[2])+
                    "\nVariety 3:"+str(counter[3])+
                    "\nVariety 4:"+str(counter[4])+
                    "\nVariety 5:"+str(counter[5])+
                    "Process End")
               break 

     # Release the webcam
     cam.release()
     stepper.ena_high()


except Exception as e:
    print(f"Error {e}")
    input()







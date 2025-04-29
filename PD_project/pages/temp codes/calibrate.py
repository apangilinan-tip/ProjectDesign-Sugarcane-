from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import os
from datetime import datetime
import threading
import array
import time
import RPi.GPIO as GPIO

from stepper import Stepper
from gpiozero import DistanceSensor
from pins import Pins
#from camera import Camera
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class CalibratePage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.initial()

    def initial(self):

        self.output = Label(self, 
            font=("Helvetica", 16, "bold"),  # Font family, size, and style
            state=DISABLED)
        self.output.pack(pady=30)  

        self.start_button = Button(self, 
            text="Startt",
            font=("Helvetica", 16, "bold"),  # Font family, size, and style
            width=20,  # Number of text characters wide
            height=2,  # Number of text lines tall
            command=self.start_setup)
        self.start_button.pack(pady=30)  

        self.bind('<Escape>', lambda e: self.master.destroy()) 


    def start_setup(self):

        self.start_button.pack_forget()
                
        #setup
        try:

            #counters counter[0]--> caneCount [6]--> waitCount
            self.counter = array.array('i',[0,0,0,0,0,0,0])

            #Pins(pin1, pin2, pin3, r1, r2, enable, start)
            self.pins = Pins(14,15,18,23,24,22,27)
            #self.pins.all_pin_low()


            #motor pins/flags ena, dir, pul
            self.stepper = Stepper(11,9,10)
            
            #ultrasonic
            self.ultrasonic = DistanceSensor(echo=17, trigger=4)

            #camera setup
            #self.cam = Camera(0)
            #self.cam.start_camera()


            self.output.config(text="Setup Complete. Proceed?\n")
            self.output.config(state=NORMAL)
            
            self.yes_button = Button(self, text="Yes", font=("Helvetica", 16, "bold"),  width=20,  height=2,                 
                    command=self.start_process)
            self.yes_button.pack( side="left", padx=10) 

            self.back_button = Button(self, text="Back", font=("Helvetica", 16, "bold"),  width=20,  height=2, 
                command=self.reload)
            self.back_button.pack( side="left", padx=10) 
 

        except Exception as e:
        
            self.output.config(text=f"Setup failed. Error {e}")
            self.output.config(state=NORMAL)

            self.yes_button = Button(self, text="Yes", font=("Helvetica", 16, "bold"),  width=20,  height=2,                 
                    command=self.start_process)
            self.back_button = Button(self, text="Back", font=("Helvetica", 16, "bold"),  
                command=self.reload)
            self.back_button.pack(pady=30) 
    
    def reload(self):
         self.yes_button.pack_forget()
         self.back_button.pack_forget()
         self.output.pack_forget()
         self.initial()
         GPIO.cleanup()


    def start_process(self):
            self.yes_button.pack_forget()
            self.back_button.pack_forget()
            self.output.pack_forget()

            self.pins_button = Button(self, text="Calibrate Pins", font=("Helvetica", 16, "bold"),width=20,height=2, 
                command=self.pins_cal)
            self.stepper_button = Button(self, text="Calibrate Stepper", font=("Helvetica", 16, "bold"),width=20,height=2, 
                command=self.step_cal)
            self.ultrasonic_button = Button(self, text="Calibrate Ultrasonic", font=("Helvetica", 16, "bold"),width=20,height=2, 
                command=self.son_cal)
            self.camera_button = Button(self, text="Calibrate Camera", font=("Helvetica", 16, "bold"),width=20,height=2, 
                command=self.cam_cal)
 
            self.pins_button.grid(row=0, column=0, padx=10, pady=10)
            self.stepper_button.grid(row=0, column=1, padx=10, pady=10)
            self.ultrasonic_button.grid(row=1, column=0, padx=10, pady=10)
            self.camera_button.grid(row=1, column=1, padx=10, pady=10)


    def pins_cal(self):
        try:
            self.pins_button.pack_forget()
            self.stepper_button.pack_forget()
            self.ultrasonic_button.pack_forget()
            self.camera_button.pack_forget()

            self.output.config(text="All pins low")
            self.output.config(state=NORMAL)
            self.pins.all_pin_low()
            time.sleep(3)

            self.output.config(text="Var 1")
            self.pins.out_to_pins(1)
            time.sleep(3)

            self.output.config(text="Var 2")
            self.pins.out_to_pins(2)
            time.sleep(3)

            self.output.config(text="Var 5")
            self.pins.out_to_pins(5)
            time.sleep(3)

            self.output.config(text="Var 3")
            self.pins.out_to_pins(5)
            time.sleep(3)

            self.output.config(text="Var 4")
            self.pins.out_to_pins(5)
            time.sleep(4)

            self.output.config(text="Reset Var")
            self.pins.reset_varPins()
            time.sleep(3)

            self.output.config(text="Relay Activate")
            self.pins.relay_activate()
            time.sleep(3)

            self.output.config(text="Relay Low")
            self.pins.relay_low()
            time.sleep(3)

            self.output.config(text="Enable High")
            self.pins.enable_high()
            time.sleep(3)

            self.output.config(text="Enable Low")
            self.pins.enable_low()
            time.sleep(3)

            self.output.config(text="Start High")
            self.pins.start_high()
            time.sleep(3)

            self.output.config(text="Start Low")
            self.pins.start_low()
            time.sleep(3)

            self.output.config(text="Done.. Returning to Menu")
            time.sleep(3)


            self.start_process()

        except Exception as e:
            self.output.config(text=f"Error {e}")
            self.output.config(state=NORMAL)
            self.back_button = Button(self, text="Back", 
                font=("Helvetica", 16, "bold"),  # Font family, size, and style
                width=20,  # Number of text characters wide
                height=2,  # Number of text lines tall
                command=self.start_process)
            self.back_button.pack(pady=30) 
    
    
    def step_cal(self):
        try:
            self.pins_button.pack_forget()
            self.stepper_button.pack_forget()
            self.ultrasonic_button.pack_forget()
            self.camera_button.pack_forget()
        
            self.output.config(text="Stepper Run, Ena Low")
            self.output.config(state=NORMAL)
            thread = threading.Thread(target=self.stepper.run, daemon=True)
            thread.start()
            self.stepper.ena_low()
            time.sleep(3)

            self.output.config(text="Stepper Run, Ena High")
            self.stepper.ena_high()
            time.sleep(3)

            self.output.config(text="Stepper Run, Ena, Dir Low")
            self.stepper.dir_low()
            self.stepper.ena_low()
            time.sleep(3)

            self.output.config(text="Stepper Run, Ena Low, Dir High")
            self.stepper.ena_high()
            self.stepper.dir_high()
            self.stepper.ena_low()
            time.sleep(3)


            self.output.config(text="Stepper Run, Ena High")
            self.stepper.ena_high()
            time.sleep(3)


            self.output.config(text="Done.. Returning to Menu")
            time.sleep(3)


            self.start_process()


        except Exception as e:
            self.output.config(text=f"Error {e}")
            self.output.config(state=NORMAL)
            self.back_button = Button(self, text="Back", 
                font=("Helvetica", 16, "bold"),  # Font family, size, and style
                width=20,  # Number of text characters wide
                height=2,  # Number of text lines tall
                command=self.start_process)
            self.back_button.pack(pady=30) 
        
        
    def son_cal(self):
        self.pins_button.grid_forget()
        self.stepper_button.grid_forget()
        self.ultrasonic_button.grid_forget()
        self.camera_button.grid_forget()
        
        try:
            self.output.config(text="Initiated")
            self.output.config(state=NORMAL)
            self.output.pack(pady=30)
            
            self.distance_button = Button(self, text="Ping", font=("Helvetica", 16, "bold"),width=20,height=2, 
                command=self.tell_dist)
 
            self.distance_button.pack(pady=30)
 
            self.back_button = Button(self, text="Back", 
                font=("Helvetica", 16, "bold"),  # Font family, size, and style
                width=20,  # Number of text characters wide
                height=2,  # Number of text lines tall
                command=self.start_process)
            self.back_button.pack(pady=30) 
   
        except Exception as e:
            self.output.config(text=f"Error {e}")
            self.output.config(state=NORMAL)
            self.back_button = Button(self, text="Back", 
                font=("Helvetica", 16, "bold"),  # Font family, size, and style
                width=20,  # Number of text characters wide
                height=2,  # Number of text lines tall
                command=self.start_process)
            self.back_button.pack(pady=30) 


    def tell_dist(self):
    
            dist = self.ultrasonic.distance
            self.output.config(text=str(dist))

            


    	

    def cam_cal(self):
        try:
            self.pins_button.pack_forget()
            self.stepper_button.pack_forget()
            self.ultrasonic_button.pack_forget()
            self.camera_button.pack_forget()

            #self.cam.capture_image("test.jpg")

            image = Image.open("test.jpg")  
            #image = image.resize((300, 300))  
            photo = ImageTk.PhotoImage(image)

            image_label = Label(self, image=photo)
            image_label.pack(pady=20)

            time.sleep(5)
            image_label.pack_forget()

            self.output.config(text="Done.. Returning to Menu")
            time.sleep(3)


            self.start_process()

        except Exception as e:
            self.output.config(text=f"Error {e}")
            self.output.config(state=NORMAL)
            self.back_button = Button(self, text="Back", 
                font=("Helvetica", 16, "bold"),  # Font family, size, and style
                width=20,  # Number of text characters wide
                height=2,  # Number of text lines tall
                command=self.start_process)
            self.back_button.pack(pady=30)






   

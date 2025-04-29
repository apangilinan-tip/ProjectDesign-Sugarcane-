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
from camera import Camera
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)




class DashboardPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)        



        self.disp = Label(self)

        image = Image.open("images/sample.jpg")
        image = image.resize((200,200))
        photo = ImageTk.PhotoImage(image)  
        self.img_disp = Label(self,image=photo)

        
        #live count
        self.livec_label = Label(self, 
                                 text = "Live Count",
                                 font = ("Lexend", 14, "bold"))        
        self.livec = Label(self, textvariable = self.counter[0])
        
        #sensor
        self.sensor_label = Label(self,
                                  text = "Sensor",
                                  font = ("Lexend", 14, "bold"))
        self.sensor_disp = Label(self, textvariable = self.sensor)
        
        #variety detected
        self.var_label = Label(self,
                               text = "Variety Detected",
                               font = ("Lexend", 14, "bold"))
        self.var_disp = Label(self, textvariable = self.vard)
        
        #conveyor actuator enable
        self.conv_disp = Label(self, text = "conv:"+str(self.conv))
        self.act_disp = Label(self, text = "actuator:"+str(self.act))
        self.ena_disp = Label(self, text = "enable:"+str(self.enable))        

        #variety counter
        self.varcount1_label = Label(self,
                                    text = "Variety 1",
                                    font = ("Lexend", 14, "bold"))        
        self.varcount2_label = Label(self,
                                    text = "Variety 2",
                                    font = ("Lexend", 14, "bold"))
        self.varcount3_label = Label(self,
                                    text = "Variety 3",
                                    font = ("Lexend", 14, "bold"))
        self.varcount4_label = Label(self,
                                    text = "Variety 4",
                                    font = ("Lexend", 14, "bold"))
        self.varcount5_label = Label(self,
                                    text = "Variety 5",
                                    font = ("Lexend", 14, "bold"))

        self.varcount1_disp = Label(self, textvariable = self.counter[1])
        self.varcount2_disp = Label(self, textvariable = self.counter[2])
        self.varcount3_disp = Label(self, textvariable = self.counter[3])
        self.varcount4_disp = Label(self, textvariable = self.counter[4])
        self.varcount5_disp = Label(self, textvariable = self.counter[5])
                                    


                
        self.img_disp.grid(    row=0, column=0, columnspan = 3, rowspan=5)
        self.livec_label.grid( row=0, column=4, columnspan = 2)
        self.livec.grid(       row=1, column=4, columnspan = 2)
        self.sensor_label.grid(row=2, column=4, columnspan = 2)
        self.sensor_disp.grid( row=3, column=4, columnspan = 2)
        self.var_label.grid(   row=4, column=4, columnspan = 2)
        self.var_disp.grid(    row=5, column=4, columnspan = 2)
        self.conv_disp.grid(   row=6, column=4, columnspan = 2)
        self.act_disp.grid(    row=7, column=4, columnspan = 2)
        self.ena_disp.grid(    row=8, column=4, columnspan = 2)
        self.disp.grid(        row=5, column=0, columnspan = 3, rowspan = 4)
        
        self.varcount1_label.grid(row=9, column=0)
        self.varcount2_label.grid(row=9, column=1)
        self.varcount3_label.grid(row=9, column=2)
        self.varcount4_label.grid(row=9, column=3)
        self.varcount5_label.grid(row=9, column=4)
        
        self.varcount1_disp.grid(row=10, column=0)
        self.varcount2_disp.grid(row=10, column=1)
        self.varcount3_disp.grid(row=10, column=2)
        self.varcount4_disp.grid(row=10, column=3)
        self.varcount5_disp.grid(row=10, column=4)
                
        self.update()        


if __name__ == "__main__":
    root = Tk()
    root.title("Dashboard Page")
    root.geometry("800x600")
    root.configure(bg="white")
    
    reports_page = DashboardPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()

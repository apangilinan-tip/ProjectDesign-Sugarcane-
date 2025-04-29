import sqlite3
import datetime
import threading
import tkinter as tk
import random

from tkinter import Frame, Tk
from gpiozero import DistanceSensor
from camera import Camera
from pins import Pins
from stepper import Stepper
from db import DbPage
from ml import MachineLearning

class DashboardPage(Frame):
    def __init__(self,  *args, **kwargs):
        super().__init__( *args, **kwargs)
        
    def start(self,counter_vars,status_vars):
        self.counter_vars = counter_vars
        self.status_vars = status_vars

        # data storage
        self.detections = []
        try:
            # Initialize hardware and components
            # Pins(varpin3, varpin2, varpin1, actuator1, actuator2, enable, start)
            #pins to arduino = varpin3, varpin2, varpin1, enable, start
            self.pins = Pins(14, 15, 18, 27, 22, 23, 24)
            self.pins.all_pin_low()
            self.stepper = Stepper(11, 9, 10)
            self.ultrasonic = DistanceSensor(echo=17, trigger=4)
            self.cam = Camera(0)
            self.cam.start_camera()
            self.db = DbPage()
            self.db.setup()
            self.ml = MachineLearning()
            #self.ml.setup()

            # Start a new session in the DB
            start_time = datetime.datetime.now().isoformat()
            self.db.cursor.execute("INSERT INTO Session (SessionName, StartTime) VALUES (?, ?)",
                                   ("Session A", start_time))
            self.db.conn.commit()
            self.session_id = self.db.cursor.lastrowid  # Get the session id for linking detections
            self.sequence = 0  # To track order within this session

            self.after(0,self.status_vars['prompt'].set("Setup Successful"))
        except Exception as e:
            self.after(0,self.status_vars['prompt'].set(f"Error during setup: {e}"))
            return
        # Start the main detection thread (to avoid blocking the GUI)
        #detection_thread = threading.Thread(target=self.run_detection_loop, daemon=True)
        #detection_thread.start()
        self.run_detection_loop()

    def status(self,var,value):
        self.status_vars[var].set(value)

    def run_detection_loop(self):
        try:
            # Start the conveyor and enable system components
            self.pins.start_high()
            self.pins.enable_low()
            self.status('system',"Detection")
            thread = threading.Thread(target=self.stepper.run, daemon=True)
            thread.start()
            self.stepper.ena_low()
            self.status('conveyor',"Running")
            self.status('actuator',"Active")
            #self.pins.relay_activate()
            self.after(4000) #temp
            self.status('actuator',"Inactive")

            # Main detection loop
            while True:

                dist = self.ultrasonic.distance
                if dist < 1:
                    self.status('sensor',round(dist, 2))
                    # Increment total cane counter
                    self.counter_vars[0].set(self.counter_vars[0].get() + 1)

                    # Build image filename
                    current_count = self.counter_vars[0].get()
                    self.imgname = f"{current_count}_cane.jpg"

                    # Capture image
                    self.cam.capture_image("images/" + self.imgname)

                    #update display
                    self.status('img',self.imgname)

                    # Reset and update system pins
                    self.pins.enable_low()
                    self.pins.reset_varPins()
                    self.status('variety',"None")

                    # Run ML detection (returns a variety as an integer, e.g., 1 to 5)
                    #self.var = self.ml.predict("images/" + self.imgname)
                    self.var = random.randint(1,5)
                    
                    # Update variety counter
                    self.counter_vars[self.var].set(self.counter_vars[self.var].get() + 1)
                    self.status('variety',str(self.var))

                    # Activate output pins based on detected variety
                    self.pins.out_to_pins(self.var)
                    self.pins.enable_high()

                    self.status('actuator',"Active")
                    self.update()
                    #self.pins.relay_activate()
                    self.after(4000)
                    self.status('actuator',"Inactive")
                    
                    # Buffer the detection event instead of immediate DB insertion
                    self.sequence += 1
                    detection_time = datetime.datetime.now().isoformat()
                    # detection_record = (self.session_id, self.sequence, detection_time, "images/" + self.imgname, self.var)
                    detection_record = (self.session_id, self.sequence, detection_time, self.imgname, self.var)
                    self.detections.append(detection_record)

                    # Reset sensor indicator for this cycle
                    self.counter_vars[6].set(0)
                    self.status('sensor',0)

                else:
                    # Increase the count for "no detection" cycles
                    self.counter_vars[6].set(self.counter_vars[6].get() + 1)

                    if self.counter_vars[6].get() == 5:
                        self.status_vars['actuator'].set("Active")
                        self.pins.relay_activate()
                        self.status_vars['actuator'].set("Inactive")
                        self.status_vars['prompt'].set("No cane detected.")
                        self.after(2000)  # Pause for 2 seconds

                    if self.counter_vars[6].get() >= 10:
                        self.pins.start_low()
                        self.status_vars['prompt'].set("No cane detected - Ending Session")
                        break  # End the loop if no cane detected for a while

            # End of session: batch insert buffered detection events
            if self.detections:
                sql = """
                    INSERT INTO Detection (session_id, sequence, detection_time, image_file, variety_id)
                    VALUES (?, ?, ?, ?, ?)
                """
                self.db.cursor.executemany(sql, self.detections)
                self.db.conn.commit()

            # Update session end time
            end_time = datetime.datetime.now().isoformat()
            self.db.cursor.execute("UPDATE Session SET end_time = ? WHERE session_id = ?",
                                   (end_time, self.session_id))
            self.db.conn.commit()

            # Cleanup hardware
            self.cam.release()
            self.stepper.ena_high()
            self.status_vars['conveyor'].set("Stopped")

        except Exception as e:
            self.status_vars['prompt'].set(f"Error during detection: {e}")

if __name__ == "__main__":
    root = Tk()
    root.title("CaneCheck")
    root.minsize(800, 600)
    root.geometry("1024x768")
    root.configure(bg="white")

    dashboard = DashboardPage(root)
    dashboard.pack(fill="both", expand=True)

    root.mainloop()


    '''
    # Raspberry Pi integration methods
    def update_sensor_status(self, status):
        self.status_vars['sensor'].set(status)
    
    def update_variety(self, variety):
        self.status_vars['variety'].set(variety)
    
    def increment_counter(self, variety_index=0):
        """Increment counters (0 = total, 1-5 = specific varieties)"""
        if 0 <= variety_index <= 5:
            self.counter_vars[variety_index].set(self.counter_vars[variety_index].get() + 1)
        if variety_index != 0:
            self.counter_vars[0].set(self.counter_vars[0].get() + 1)'''

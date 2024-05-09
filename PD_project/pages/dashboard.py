from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import os
from datetime import datetime
import threading
from pymongo import MongoClient
from tkinter import simpledialog
from config import MONGODB_URI
import base64

class DashboardPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
    
        self.vid = cv2.VideoCapture(0) 
        self.width, self.height = 800, 600
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width) 
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height) 

        # Create a label for the camera preview
        self.label_widget = Label(self, borderwidth=5, relief="ridge")
        self.label_widget.grid(row=1, column=0, padx=10, pady=10)  

        self.capture_image = False
        self.image_count = 0
        self.capture_start_time = None
        self.capture_end_time = None  # Initialize capture end time

        # Create a label to display the image count
        self.count_label = Label(self, text="Images captured: 0")
        self.count_label.grid(row=1, column=1, padx=10, pady=10)  

        # Create a button to capture an image
        self.capture_button = Button(self, text="Capture Image", command=self.toggle_capture)
        self.capture_button.grid(row=3, column=0, padx=10, pady=10)  

        # Create a button to stop capturing
        self.stop_button = Button(self, text="Stop Capture", command=self.stop_capture, state=DISABLED)
        self.stop_button.grid(row=4, column=0, padx=10, pady=10)  

        self.bind('<Escape>', lambda e: self.master.destroy()) 

        # Start the camera preview thread
        self.camera_thread = threading.Thread(target=self.open_camera)
        self.camera_thread.daemon = True
        self.camera_thread.start()

        self.session_detail_list = [] 
        self.initialize_database()

    def open_camera(self): 
        while True:
            ret, frame = self.vid.read()  # Capture the video frame by frame
            if ret:  # Check if the frame is valid
                opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
                captured_image = Image.fromarray(opencv_image)  
                photo_image = ImageTk.PhotoImage(image=captured_image) 
                self.label_widget.photo_image = photo_image 
                self.label_widget.configure(image=photo_image) 
                self.label_widget.image = photo_image  # Keep a reference to prevent garbage collection

    def toggle_capture(self):
        if not self.capture_image:
            self.capture_button.config(text="Capturing...")
            self.stop_button.config(state=NORMAL)
            self.capture_image = True
            self.capture_start_time = datetime.now()  # Capture the start time
            self.capture_images_continuously()
        else:
            self.capture_button.config(text="Capture Image")
            self.stop_button.config(state=DISABLED)
            self.capture_image = False
            self.stop_capture()  # Stop capture and persist data

    def stop_capture(self):
        if self.capture_image:
            self.capture_button.config(text="Capture Image")
            self.stop_button.config(state=DISABLED)
            self.capture_image = False
            self.capture_end_time = datetime.now()  # Capture the end time
            self.ask_session_name()  # Ask for session name
            self.session_detail_list.clear()  # Clear session detail list
            self.capture_start_time = None  # Reset capture start time
            self.capture_end_time = None   # Reset capture end time

    def capture_images_continuously(self):
        if self.capture_image:
            self.capture_image_func()  # Capture an image
            self.master.after(5000, self.capture_images_continuously)  # Capture image every 5 seconds

    def capture_image_func(self):
        ret, frame = self.vid.read()
        if ret:
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
            captured_image = Image.fromarray(opencv_image) 
            self.save_image(captured_image)
            self.image_count += 1
            self.count_label.config(text=f"Images captured: {self.image_count}")

    def save_image(self, image):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        session_path = os.path.join("captured_images")
        if not os.path.exists(session_path):
            os.makedirs(session_path)
        image_filename = f"sugarcane_image_{timestamp}.png"
        image.save(os.path.join(session_path, image_filename))
    
        # Convert image to base64
        with open(os.path.join(session_path, image_filename), "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        
        self.session_detail_list.append(image_base64)

    def initialize_database(self):
        self.client = MONGODB_URI  # Connect to MongoDB
        self.db = self.client["CaneCheck"]  # Select the database
        self.session_table = self.db["Session"]  # Select the collection
        self.session_detail_table = self.db["SessionDetail"] 

    def ask_session_name(self):
        # Ask user to input session name
        session_name = simpledialog.askstring("Input", "Enter session name:")
        if session_name:
            self.persist_to_database(session_name)

    def persist_to_database(self, session_name):
        if self.image_count > 0 and session_name:
            # Increment session ID
            self.current_session_id = self.get_next_session_id()  # Get the next available session ID

            # Insert new data into MongoDB
            session_data = {
                "Session_ID": self.current_session_id,
                "SessionName": session_name,
                "StartTime": self.capture_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "EndTime": self.capture_end_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.session_table.insert_one(session_data)  # Insert data into MongoDB collection

            for file_name in self.session_detail_list:
                variety_id = self.determine_variety_id(file_name)
                session_detail_data = {
                    "Session_ID": self.current_session_id,
                    "Sequence": file_name,
                    "Variety_ID": variety_id
                }
                self.session_detail_table.insert_one(session_detail_data)


    def get_next_session_id(self):
        # Get the next available session ID
        last_session = self.session_table.find_one(sort=[("Session_ID", -1)])  # Get the document with the highest session ID
        if last_session:
            return last_session["Session_ID"] + 1
        else:
            return 1

    def determine_variety_id(self, filename):  
        # Enter your code here to process the image on open cv
        return "variety1" 

    def exit_app(self):
        self.vid.release()  # Release the camera
        self.master.destroy()
    
if __name__ == "__main__":
    root = Tk()
    root.title("Dashboard Page")
    root.geometry("800x600")
    root.configure(bg="white")
    
    reports_page = DashboardPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()
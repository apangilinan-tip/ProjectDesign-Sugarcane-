from tkinter import *
import cv2
from PIL import Image, ImageTk
import os
from datetime import datetime
import threading
import base64
from tkinter import simpledialog, messagebox
import queue
import sqlite3

class DashboardPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.vid = cv2.VideoCapture(0)
        self.width, self.height = 320, 150
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        # Create a label for the camera preview
        self.label_widget = Label(self, borderwidth=5, relief="ridge")
        self.label_widget.grid(row=1, column=0, padx=10, pady=10)

        self.capture_image = False
        self.image_count = 0
        self.capture_start_time = None
        self.capture_end_time = None

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

        # Queue to pass captured images from camera thread to main GUI thread
        self.image_queue = queue.Queue()

        self.session_detail_list = []
        self.initialize_database()

        # Start the camera preview thread
        self.camera_thread = threading.Thread(target=self.open_camera)
        self.camera_thread.daemon = True
        self.camera_thread.start()
        self.update_camera()  # Start updating the camera preview

    def initialize_database(self):
        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('sessiondb.db')
        self.cursor = self.conn.cursor()

        # Create a combined table for both session and image data
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SessionDB (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                SessionName TEXT,
                StartTime TEXT,
                EndTime TEXT,
                Sequence INTEGER,
                FileName TEXT,
                Variety_ID TEXT,
                ImageData TEXT  -- To store the base64 image data
            )
        ''')

        self.conn.commit()

    def open_camera(self):
        while True:
            ret, frame = self.vid.read()  # Capture the video frame by frame
            if ret:  # Check if the frame is valid
                opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                opencv_image = cv2.resize(opencv_image, (self.width, self.height))
                captured_image = Image.fromarray(opencv_image)
                # Put the captured image into the queue
                self.image_queue.put(captured_image)

    def update_camera(self):
        if not self.image_queue.empty():
            captured_image = self.image_queue.get()
            photo_image = ImageTk.PhotoImage(image=captured_image)
            self.label_widget.photo_image = photo_image
            self.label_widget.configure(image=photo_image)
            self.label_widget.image = photo_image
        self.label_widget.after(10, self.update_camera)  # Schedule the next update

    def refresh_app(self):
        self.capture_image = False
        self.image_count = 0
        self.capture_start_time = None
        self.capture_end_time = None
        self.session_detail_list = []

        self.capture_button.config(text="Capture Image", state=NORMAL)
        self.stop_button.config(state=DISABLED)
        self.count_label.config(text="Images captured: 0")
        
        self.update_camera()

    def toggle_capture(self):
        if not self.capture_image:
            self.capture_button.config(text="Capturing...")
            self.stop_button.config(state=NORMAL)
            self.capture_image = True
            self.capture_start_time = datetime.now()  # Capture the start time
            self.after(5000, self.capture_images_continuously)
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
            self.capture_end_time = None   # Reset end time
            self.refresh_app()  # Refresh the app to reset everything

    def capture_images_continuously(self):
        if self.capture_image:
            self.capture_image_func()  # Capture an image
            self.master.after(5000, self.capture_images_continuously)  # Capture image every 5 seconds

    def capture_image_func(self):
        ret, frame = self.vid.read()
        if ret:
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            captured_image = Image.fromarray(opencv_image)
            filename, image_base64 = self.save_image(captured_image)
            self.session_detail_list.append((filename, image_base64))  # Append both filename and base64
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
        
        return image_filename, image_base64  # Return both the filename and base64


    def ask_session_name(self):
        while True:
            session_name = simpledialog.askstring("Input", "Enter session name:")  # Ask user to input session name
            if session_name:
                self.cursor.execute("SELECT 1 FROM SessionDB WHERE SessionName = ?", (session_name,))
                if self.cursor.fetchone():
                    result = messagebox.askyesno("Duplicate Session Name", "Session name already exists. Do you want to enter a different name?")  # Session name already exists, ask if the user wants to try again or cancel
                    if not result:  # User chose not to enter a different name, exit the loop
                        return
                else:
                    self.persist_to_database(session_name)  # Session name is unique, proceed to persist to database
                    return
            else:
                return  # User canceled the operation, exit the loop without saving the session details

    def persist_to_database(self, session_name):
        if self.image_count > 0 and session_name:
            sequence = 0
            for file_name, image_base64 in self.session_detail_list:
                sequence += 1
                variety_id = self.determine_variety_id(file_name)
                self.cursor.execute("INSERT INTO SessionDB (SessionName, StartTime, EndTime, Sequence, FileName, Variety_ID, ImageData) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                    (session_name, self.capture_start_time.strftime("%Y-%m-%d %H:%M:%S"), 
                                    self.capture_end_time.strftime("%Y-%m-%d %H:%M:%S"), sequence, file_name, variety_id, image_base64))
            self.conn.commit()

    def determine_variety_id(self, filename):  
        # Enter your code here to process the image with OpenCV and determine the variety
        return "variety1"

    def exit_app(self):
        self.vid.release()  # Release the camera
        self.conn.close()  # Close the database connection
        self.master.destroy()

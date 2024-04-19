from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import os
from datetime import datetime
import threading

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
            self.capture_start_time = datetime.now()  # Set the start time
            self.capture_images_continuously()
        else:
            self.capture_button.config(text="Capture Image")
            self.stop_button.config(state=DISABLED)
            self.capture_image = False

    def capture_images_continuously(self):
        if self.capture_image:
            current_time = datetime.now()
            time_difference = current_time - self.capture_start_time
            if time_difference.total_seconds() >= 5:  # Check if 5 seconds have passed
                self.capture_start_time = current_time  # Update the start time
                self.capture_image_func()  # Capture an image
            self.master.after(10, self.capture_images_continuously)  # Continue capturing images

    def capture_image_func(self):
        ret, frame = self.vid.read()
        if ret:
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
            captured_image = Image.fromarray(opencv_image) 
            self.save_image(captured_image)
            self.image_count += 1
            self.count_label.config(text=f"Images captured: {self.image_count}")

    def stop_capture(self):
        self.capture_button.config(text="Capture Image")
        self.stop_button.config(state=DISABLED)
        self.capture_image = False

    def save_image(self, image):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        session_path = os.path.join("captured_images")
        if not os.path.exists(session_path):
            os.makedirs(session_path)
        image.save(os.path.join(session_path, f"sugarcane_image_{timestamp}.png"))

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

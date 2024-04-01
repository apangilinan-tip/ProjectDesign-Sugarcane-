from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import os

from datetime import datetime

class DashboardPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        label = Label(self, text="Dashboard Page")
        label.grid(row=0, column=0, columnspan=2, pady=10)

        self.vid = cv2.VideoCapture(0) 
        self.width, self.height = 800, 600
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width) 
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height) 

        # Create a label for the camera preview
        self.label_widget = Label(self, borderwidth=5, relief="ridge")
        self.label_widget.grid(row=1, column=0, padx=10, pady=10)  

        self.capture_image = False
        self.image_count = 0

        # Create a label to display the image count
        self.count_label = Label(self, text="Images captured: 0")
        self.count_label.grid(row=2, column=0, padx=10, pady=10)  

        # Create a button to capture an image
        self.button1 = Button(self, text="Capture Image", command=self.capture_image_func)
        self.button1.grid(row=3, column=0, padx=10, pady=10)  

        self.bind('<Escape>', lambda e: self.master.destroy()) 

        self.open_camera()  # Start the camera preview

    def open_camera(self): 
        # Capture the video frame by frame 
        _, frame = self.vid.read() 
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
        captured_image = Image.fromarray(opencv_image)  
        photo_image = ImageTk.PhotoImage(image=captured_image) 
        self.label_widget.photo_image = photo_image 
        self.label_widget.configure(image=photo_image) 

        if not self.capture_image:  # If not capturing an image, update the preview
            self.label_widget.after(10, self.open_camera) 
        else:  # Save the image and update the count
            self.image_count += 1
            self.save_image(captured_image)
            self.count_label.config(text=f"Images captured: {self.image_count}")
            self.capture_image = False  # Reset the flag
            self.label_widget.after(10, self.open_camera)  # Continue capturing image

    def capture_image_func(self):
        self.capture_image = True  # Set the flag to capture an image

    def save_image(self, image):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        session_path = os.path.join("captured_images")
        if not os.path.exists(session_path):
            os.makedirs(session_path)
        image.save(os.path.join(session_path, f"sugarcane_image_{timestamp}.png"))

    def exit_app(self):
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    root.title("Dashboard Page")
    root.geometry("800x600")
    root.configure(bg="white")
    
    reports_page = DashboardPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()

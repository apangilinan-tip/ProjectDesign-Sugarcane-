from tkinter import *
import cv2 
from PIL import Image, ImageTk 

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
        self.label_widget.grid(row=1, column=0, padx=10, pady=10)  # Adjust the values of padx and pady as needed

        self.capture_image = False

        # Create a button to capture an image
        self.button1 = Button(self, text="Capture Image", command=self.capture_image_func)
        self.button1.grid(row=2, column=0, padx=10, pady=10)  # Adjust the values of padx and pady as needed

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

    def capture_image_func(self):
        self.capture_image = True  # Set the flag to capture an image

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

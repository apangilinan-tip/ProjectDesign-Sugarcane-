import cv2

class Camera:
    def __init__(self, index):
        self.index = index
    
    def start_camera(self):
        self.cap = cv2.VideoCapture(self.index)

        if not self.cap.isOpened():
            raise ValueError("Error: Could not open the webcam.")
    

    def capture_image(self, output_path="captured_image.jpg"):
    
        ret, frame = self.cap.read()    # Read a frame from the webcam

        if ret:
            # Save the image to the specified path
            cv2.imwrite(output_path, frame)
            print(f"Image captured and saved as {output_path}")
        else:
            raise ValueError("Error: Could not capture an image.")
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
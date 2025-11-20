import cv2
from PIL import Image, ImageTk
import time

class Camera():
    def __init__(self, view, model):
        """
        Initializes the camera for video capture.
        """
        self.camera = cv2.VideoCapture(0)
        self.view = view
        self.model = model

    def update(self):
        """
        Captures a frame from the camera, processes it, and updates the view.
        """
        ret, frame = self.camera.read()
        if ret:
            #==============================
            #If you want to fix camera size, modify this line.
            frame = cv2.resize(frame, (600, 400))
            #==============================
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.model.detect_video_frame(frame, int(time.time() * 1000))

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.view.imgtk = imgtk
            self.view.configure(image=imgtk)

        self.view.after(10, self.update)

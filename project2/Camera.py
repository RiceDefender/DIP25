import cv2
from PIL import Image, ImageTk
import threading
import time

class Camera:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.camera = cv2.VideoCapture(0)
        self.running = True
        self.latest_frame = None

        # start a new thread
        self.capture_thread = threading.Thread(target=self.capture_loop, daemon=True)
        self.capture_thread.start()

        # start ui update loop on main thread
        self.update_ui()

    def capture_loop(self):
        """Camera capture loop (on a separate thread)"""
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.latest_frame = frame

            # run inference on a new thread
            threading.Thread(
                target=self.model.detect_video_frame,
                args=(self.latest_frame, int(time.time()*1000)),
                daemon=True
            ).start()

    def update_ui(self):
        """Updates UI (on main thread)"""
        if self.latest_frame is not None:
            img = Image.fromarray(self.latest_frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.view.imgtk = imgtk
            self.view.configure(image=imgtk)

        self.view.after(10, self.update_ui)

    def stop(self):
        self.running = False
        if self.camera:
            self.latest_frame = None
            self.camera.release()
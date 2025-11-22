import cv2
from PIL import Image, ImageTk
import threading
import time
import numpy as np
from draw_utils import draw_landmarks, display_brush_size

class Camera:
    def __init__(self, view, model, drawer=None, drawing_canvas=None):
        """
        Initializes the camera for video capture.
        """
        self.camera = cv2.VideoCapture(0)
        self.view = view
        self.model = model
        self.drawer = drawer
        self.drawing_canvas = drawing_canvas

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

                    # Convert normalized coordinates to canvas coordinates
                    canvas_w = self.drawing_canvas.winfo_width()
                    canvas_h = self.drawing_canvas.winfo_height()
                    x = int(index_finger_tip.x * canvas_w)
                    y = int(index_finger_tip.y * canvas_h)

                    # Update the drawer with the current brush thickness
                    self.drawer.update(x, y, is_drawing, self.model.brush_thickness)

                    # Update the drawing canvas display
                    updated_canvas = self.drawer.get_canvas()
                    pil_img = Image.fromarray(cv2.cvtColor(updated_canvas, cv2.COLOR_BGR2RGB))
                    tk_img = ImageTk.PhotoImage(pil_img)
                    self.drawing_canvas.create_image(0, 0, anchor="nw", image=tk_img)
                    self.drawing_canvas.tk_canvas_image = tk_img  # Prevent garbage collection

            # Update camera view
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.view.imgtk = imgtk
            self.view.configure(image=imgtk)

        self.view.after(10, self.update_ui)

    def stop(self):
        self.running = False
        if self.camera:
            self.latest_frame = None
            self.camera.release()
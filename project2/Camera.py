import cv2
from PIL import Image, ImageTk
import time
import numpy as np
from draw_utils import draw_landmarks

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

    def update(self):
        """
        Captures a frame from the camera, processes it, and updates the view.
        """
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.resize(frame, (600, 400))
            
            detection_result = self.model.detect_video_frame(frame, int(time.time() * 1000))

            # Draw landmarks on the frame
            if detection_result:
                draw_landmarks(frame, detection_result)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if self.drawer and self.drawing_canvas and detection_result:
                self.model.update_gesture(detection_result)
                is_drawing = self.model.is_pinching

                if detection_result.hand_landmarks:
                    landmarks = detection_result.hand_landmarks[0]
                    index_finger_tip = landmarks[8]  # Index finger tip

                    # Convert normalized coordinates to canvas coordinates
                    canvas_w = self.drawing_canvas.winfo_width()
                    canvas_h = self.drawing_canvas.winfo_height()
                    x = int(index_finger_tip.x * canvas_w)
                    y = int(index_finger_tip.y * canvas_h)

                    self.drawer.update(x, y, is_drawing)

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

        self.view.after(10, self.update)

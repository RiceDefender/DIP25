import cv2
import numpy as np

class Renderer:
    def __init__(self, drawer):
        self.drawer = drawer

    def render(self, frame):
        canvas = self.drawer.get_canvas()
        # Ensure canvas is the same size as the frame
        if canvas.shape != frame.shape:
            canvas = cv2.resize(canvas, (frame.shape[1], frame.shape[0]))
        
        # Combine frame and canvas
        combined_frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
        return combined_frame

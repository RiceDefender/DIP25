import cv2
import numpy as np
import mediapipe as mp

# MediaPipe hands solution for HAND_CONNECTIONS
mp_hands = mp.solutions.hands

class Drawer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
        self.draw_color = (0, 0, 0)  # Default to black
        self.thickness = 5
        self.prev_x, self.prev_y = None, None

    def update(self, x, y, is_drawing, thickness):
        self.thickness = thickness
        if is_drawing:
            if self.prev_x is not None and self.prev_y is not None:
                cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y), self.draw_color, self.thickness)
            self.prev_x, self.prev_y = x, y
        else:
            self.prev_x, self.prev_y = None, None

    def clear(self):
        self.canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255

    def get_canvas(self):
        return self.canvas

def draw_landmarks(frame, detection_result):
    if not (detection_result and detection_result.hand_landmarks):
        return

    height, width, _ = frame.shape
    
    for hand_landmarks in detection_result.hand_landmarks:
        # Draw landmark points
        for landmark in hand_landmarks:
            point = (int(landmark.x * width), int(landmark.y * height))
            cv2.circle(frame, point, 4, (121, 22, 76), -1) # Draw a filled circle for each landmark

        # Draw connections
        if mp_hands.HAND_CONNECTIONS:
            for connection in mp_hands.HAND_CONNECTIONS:
                start_idx = connection[0]
                end_idx = connection[1]
                
                # Ensure landmarks are within bounds
                if start_idx < len(hand_landmarks) and end_idx < len(hand_landmarks):
                    start_landmark = hand_landmarks[start_idx]
                    end_landmark = hand_landmarks[end_idx]
                    
                    start_point = (int(start_landmark.x * width), int(start_landmark.y * height))
                    end_point = (int(end_landmark.x * width), int(end_landmark.y * height))
                    
                    cv2.line(frame, start_point, end_point, (250, 44, 250), 2)

def display_brush_size(frame, brush_size):
    """ Displays the current brush size on the top-left of the frame. """
    text = f"Brush Size: {brush_size}px"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

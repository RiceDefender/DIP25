import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "hand_landmarker.task") #Absolute path

class Model():
    def __init__(self, use_gpu=False):
        """
        Initializes the HandLandmarker model.

        Args:
            use_gpu (bool): whether to attempt using the GPU
        """
        try:
            # try to use GPU
            delegate = python.BaseOptions.Delegate.GPU if use_gpu else python.BaseOptions.Delegate.CPU
            base_options = python.BaseOptions(
                model_asset_path=MODEL_PATH,
                delegate=delegate
            )
        except RuntimeError as e:
            # use CPU if GPU is not available
            print(f"Failed to initialize with GPU ({e}). Falling back to CPU.")
            base_options = python.BaseOptions(
                model_asset_path=MODEL_PATH,
                delegate=python.BaseOptions.Delegate.CPU
            )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            num_hands=1
        )

        # initialize attributes
        self.detector    = vision.HandLandmarker.create_from_options(options)
        self.gesture     = None
        self.prev_pos    = None
        self.is_pinching = None
        self.brush_thickness = 5

    def detect_video_frame(self, frame, timestamp):
        """
        Detects hand landmarks in a video frame.

        Args:
            frame: bgr video frame
            timestamp: timestep in ms

        Returns:
            A HandLandmarkerResult object or None if an error occurs.
        """
        try:
            # create a MediaPipe image object
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            
            # detect hand landmarks
            detection_result = self.detector.detect_for_video(mp_image, timestamp)
            self.update_gesture(detection_result)
            
            return detection_result
        except Exception as e:
            print(f"Error during frame detection: {e}")
            return None

    def update_gesture(self, detection_result):
        """
        Updates detected gesture.

        Args:
            detection_result: landmark detection result
        """
        # return None if hands are not detected
        if not detection_result.hand_landmarks:
            self.gesture = None
            return

        # use the detection result from the first hand
        landmarks = detection_result.hand_landmarks[0]

        # use the tip of the index finger for gesture recognition
        eps = 0.05
        thumb_x = landmarks[4].x
        thumb_y = landmarks[4].y
        fingertip_x = landmarks[8].x
        fingertip_y = landmarks[8].y

        # check if pinching
        if abs(thumb_x - fingertip_x) < eps and abs(thumb_y - fingertip_y) < eps:
            self.is_pinching = True
            self.gesture = "pinching"
        else:
            self.is_pinching = False

        # --- Brush size mapping ---
        if not self.is_pinching:
            fingers_up = []
            # Map finger for brush size
            if landmarks[8].y < landmarks[6].y:
                fingers_up.append("INDEX")
            if landmarks[12].y < landmarks[10].y:
                fingers_up.append("MIDDLE")
            if landmarks[16].y < landmarks[14].y:
                fingers_up.append("RING")
            if landmarks[20].y < landmarks[18].y:
                fingers_up.append("PINKY")

            num_fingers_up = len(fingers_up)

            # Map finger to brush size
            if num_fingers_up == 1:
                self.brush_thickness = 5
            elif num_fingers_up == 2:
                self.brush_thickness = 10
            elif num_fingers_up == 3:
                self.brush_thickness = 12
            elif num_fingers_up == 4:
                self.brush_thickness = 18

    def get_gesture(self):
        """ Returns detected gesture """
        return self.gesture

    def close(self):
        """ Closes the hand landmarker detector """
        if hasattr(self, 'detector'):
            self.detector.close()

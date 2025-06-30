# app/camera_module.py
import cv2

class Camera:
    def __init__(self, cam_index=0):
        self.cap = cv2.VideoCapture(cam_index)

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("[Camera] Failed to capture frame.")
        return frame

    def release(self):
        self.cap.release()

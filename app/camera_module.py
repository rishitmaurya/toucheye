# app/camera_module.py
import cv2

class Camera:
    def __init__(self, cam_index=0):
        try:
            self.cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)  # Windows DirectShow

            if not self.cap.isOpened():
                raise RuntimeError("Error: Could not open video capture.")

            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer size

            print("[Camera] Initialized with DirectShow backend, 1280x720 @30 FPS")
        except Exception as e:
            print(f"[Camera] Error initializing camera: {str(e)}")
            raise e

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("[Camera] Failed to capture frame.")
        return frame

    def release(self):
        if self.cap.isOpened():
            self.cap.release()

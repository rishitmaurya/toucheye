# app/vision_module.py
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

class Vision:
    def __init__(self, master_image_path):
        self.master_color = cv2.imread(master_image_path)
        if self.master_color is None:
            raise ValueError(f"[Vision] Master image not found at {master_image_path}")

        self.master_gray = cv2.cvtColor(self.master_color, cv2.COLOR_BGR2GRAY)
        self.sift = cv2.SIFT_create()
        self.kp_master, self.des_master = self.sift.detectAndCompute(self.master_gray, None)
        self.matcher = cv2.BFMatcher()

    def compare(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp_frame, des_frame = self.sift.detectAndCompute(frame_gray, None)

        if des_frame is None or self.des_master is None:
            print("[Vision] No features detected.")
            return 0.0, frame

        matches = self.matcher.knnMatch(self.des_master, des_frame, k=2)

        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        match_ratio = len(good_matches) / len(self.kp_master) if len(self.kp_master) > 0 else 0
        match_percentage = match_ratio * 100

        print(f"[Vision] SIFT good matches: {len(good_matches)} / {len(self.kp_master)} => {match_percentage:.2f}%")

        # Draw matches for visualization
        result_img = cv2.drawMatches(
            self.master_color, self.kp_master, frame, kp_frame, good_matches, None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )

        # --- SSIM for fine-grained difference detection ---
        ssim_score, diff = ssim(self.master_gray, frame_gray, full=True)
        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        return match_percentage, result_img
    
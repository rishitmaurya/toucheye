import cv2
import numpy as np

class ImageComparator:
    def __init__(self, master_img_path):
        # Load and prepare the master image
        self.master_img = cv2.imread(master_img_path)
        if self.master_img is None:
            raise ValueError(f"Could not load image at path: {master_img_path}")
        self.master_img = cv2.resize(self.master_img, (640, 480))
        self.master_gray = cv2.cvtColor(self.master_img, cv2.COLOR_BGR2GRAY)

        # Initialize AKAZE detector
        self.akaze = cv2.AKAZE_create()
        self.kp1, self.des1 = self.akaze.detectAndCompute(self.master_gray, None)
        self.detection_enabled = False

    def start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                print("Error: Could not open video capture.")
                return

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            self.detection_enabled = True
            print("Camera started successfully.")
            self.process_frames()

        except Exception as e:
            print(f"Error starting camera: {str(e)}")

    def akaze_match(self, frame_gray):
        """Aligns the frame to the master image using AKAZE keypoints and returns similarity."""
        kp2, des2 = self.akaze.detectAndCompute(frame_gray, None)

        if des2 is None or self.des1 is None:
            return None, 0

        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.knnMatch(self.des1, des2, k=2)

        good_matches = []
        for match in matches:
            if len(match) == 2:
                m, n = match
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)


        if len(good_matches) >= 10:
            src_pts = np.float32([self.kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
            if H is not None:
                aligned = cv2.warpPerspective(frame_gray, H, (640, 480))

                # Pixel-wise absolute difference
                diff = cv2.absdiff(self.master_gray, aligned)
                _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

                total_pixels = thresh.size
                non_zero_pixels = np.count_nonzero(thresh)
                similarity = ((total_pixels - non_zero_pixels) / total_pixels) * 100

                return aligned, similarity

        return None, 0

    def process_frames(self):
        while self.detection_enabled:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            frame_resized = cv2.resize(frame, (640, 480))
            frame_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

            aligned_frame, similarity = self.akaze_match(frame_gray)

            if aligned_frame is not None:
                diff_img = cv2.absdiff(self.master_gray, aligned_frame)
                stacked = cv2.hconcat([
                    self.master_gray,
                    aligned_frame,
                    diff_img
                ])
                cv2.putText(stacked, f"Similarity: {similarity:.2f}%", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
                cv2.imshow("AKAZE Aligned Comparison", stacked)
            else:
                cv2.imshow("AKAZE Aligned Comparison", frame_resized)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

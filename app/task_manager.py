# app/task_manager.py
class TaskManager:
    def __init__(self, camera, vision, logger, threshold):
        self.camera = camera
        self.vision = vision
        self.logger = logger
        self.threshold = threshold  

    def run_task(self):
        print("[TaskManager] Capturing image...")
        frame = self.camera.capture_frame()
        score, result_img = self.vision.compare(frame)  

        print(f"[TaskManager] Comparing: score={score:.2f}% vs threshold={self.threshold}%")

        if score >= self.threshold:
            result = "PASS"
        else:
            result = "FAIL"

        self.logger.log("VisionTest", result, score)
        return result, score, result_img

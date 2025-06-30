# app/gui.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2

class MainWindow(QWidget):
    def __init__(self, task_manager):
        super().__init__()
        self.setWindowTitle("TouchEye - SIFT Vision Tester")
        self.task_manager = task_manager
        self.camera = task_manager.camera
        self.master_image = task_manager.vision.master_color

        self.layout = QVBoxLayout()

        self.status_label = QLabel("Status: Ready")
        self.layout.addWidget(self.status_label)

        # Layout for images
        self.images_layout = QHBoxLayout()

        self.master_image_label = QLabel()
        self.images_layout.addWidget(self.master_image_label)

        self.camera_image_label = QLabel()
        self.images_layout.addWidget(self.camera_image_label)

        self.result_image_label = QLabel()
        self.images_layout.addWidget(self.result_image_label)

        self.layout.addLayout(self.images_layout)

        self.test_button = QPushButton("Run Vision Test")
        self.test_button.clicked.connect(self.run_test)
        self.layout.addWidget(self.test_button)

        self.btn_exit = QPushButton("Exit")
        self.btn_exit.clicked.connect(self.close)
        self.layout.addWidget(self.btn_exit)

        self.setLayout(self.layout)

        # Show master image once
        self.display_image(self.master_image, self.master_image_label)

        # Live camera preview
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera_view)
        self.timer.start(30)  # ~30 FPS

    def update_camera_view(self):
        try:
            frame = self.camera.capture_frame()
            self.display_image(frame, self.camera_image_label)
        except:
            pass

    def run_test(self):
        result, score, result_img = self.task_manager.run_task()
        self.update_status(f"{result} (Similarity: {score:.1f}%)")
        self.display_image(result_img, self.result_image_label)

    def display_image(self, frame, label):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qt_image).scaled(400, 300))

    def update_status(self, msg):
        self.status_label.setText(f"Status: {msg}")

# app/main.py
import sys
from PyQt5.QtWidgets import QApplication
from app.config import Config
from app.camera_module import Camera
from app.vision_module import Vision
from app.logger import Logger
from app.task_manager import TaskManager
from app.gui import MainWindow

def main():
    cfg = Config()
    cam = Camera()
    vision = Vision("resources/master_images/roof.jpg")
    logger = Logger()
    task_manager = TaskManager(cam, vision, logger, cfg.threshold)

    app = QApplication(sys.argv)
    window = MainWindow(task_manager)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

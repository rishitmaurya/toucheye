# app/logger.py
import csv
import os
import datetime

class Logger:
    def __init__(self, log_file="logs/test_log.csv"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.isfile(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "step", "result", "score"])

    def log(self, step, result, score):
        now = datetime.datetime.now().isoformat()
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now, step, result, score])
        print(f"[Logger] Logged: {step}, {result}, {score:.4f}")

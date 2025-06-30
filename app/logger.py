# app/logger.py
import csv
import datetime

class Logger:
    def __init__(self, log_file="logs/test_log.csv"):
        self.log_file = log_file

    def log(self, step, result, score):
        now = datetime.datetime.now().isoformat()
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now, step, result, score])
        print(f"[Logger] Logged: {step}, {result}, {score:.4f}")

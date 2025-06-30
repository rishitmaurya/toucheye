# app/config.py
import yaml

class Config:
    def __init__(self, path="config.yaml"):
        with open(path, 'r') as file:
            cfg = yaml.safe_load(file)
        self.threshold = cfg.get("threshold", 15)

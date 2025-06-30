# app/robot_comm.py
import socket

class RobotComm:
    def __init__(self, robot_ip, robot_port):
        self.robot_ip = robot_ip
        self.robot_port = robot_port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.robot_ip, self.robot_port))
        print(f"[RobotComm] Connected to robot at {self.robot_ip}:{self.robot_port}")

    def send_message(self, msg):
        self.sock.sendall(msg.encode())
        print(f"[RobotComm] Sent: {msg}")

    def receive_message(self):
        data = self.sock.recv(1024)
        msg = data.decode()
        print(f"[RobotComm] Received: {msg}")
        return msg

    def close(self):
        if self.sock:
            self.sock.close()

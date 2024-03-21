import socket


class CommunicatorClient:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode())
        except Exception as e:
            print("Error occurred while sending message:", e)

    def recv_message(self):
        try:
            data = self.socket.recv(1024)
            return data.decode()  # Return the received message as a string
        except Exception as e:
            print("Error occurred while receiving message:", e)
            return None

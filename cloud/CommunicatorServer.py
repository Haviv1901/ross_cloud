import socket


class CommunicatorServer:
    HOST = "0.0.0.0"  # Listen on all available interfaces
    PORT = 6969

    def __init__(self):
        self.socket = None

    def start_listening(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind((self.HOST, self.PORT))
        client_socket.listen(1)  # Listen for only one connection
        print(f"Server listening on {self.HOST}:{self.PORT}")
        self.socket, client_address = client_socket.accept()
        print(f"Connection established with {client_address}")

    def send_message(self, message):
        print("Sending:", message)
        try:
            if self.socket:
                self.socket.sendall(message.encode())
        except Exception as e:
            print("Error occurred while sending message:", e)

    def recv_message(self):
        try:
            data = self.socket.recv(1024)
            data = data.decode()
            print("Received:", data)
            return data  # Return the received message as a string
        except Exception as e:
            print("Error occurred while receiving message:", e)
            return None

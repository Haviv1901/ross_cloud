from CommunicatorClient import CommunicatorClient


class CloudManager:

    PORT = 6969
    HOST = "localhost"

    def __init__(self):
        self.username = ""
        self.communicator = CommunicatorClient(self.HOST, self.PORT)

    def start_connection(self):
        communicator = CommunicatorClient(self.HOST, self.PORT)

    def cloud_login(self, username, password):
        msg = "login," + username + "," + password
        self.communicator.send_message(msg)
        response = self.communicator.recv_message()
        if response == "1":
            self.username = self.communicator.recv_message()
            return True
        else:
            return False

    def cloud_register(self, username, password):
        msg = "register," + username + "," + password
        self.communicator.send_message(msg)
        response = self.communicator.recv_message()
        if response == "1":
            self.username = self.communicator.recv_message()
            return True
        else:
            return False

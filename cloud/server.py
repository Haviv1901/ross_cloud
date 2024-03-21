from CommunicatorServer import CommunicatorServer
from User import User
from DatabaseManager import UsersDataBase


class ServerManager:

    def __init__(self):
        # init socket and start listening on port
        self.com = CommunicatorServer()
        self.com.start_listening()
        # init database
        self.user_db = UsersDataBase()

        self.start()

    def start(self):
        while True:
            msg = self.com.recv_message()
            data_list = msg.split(',')

            if (data_list[0] != "login" and data_list[0] != "register"):  # check for register
                self.com.send_message("0")
                continue

            user_trying_auth = User(data_list[1], data_list[2])
            if data_list[0] == "login":
                self.try_login(user_trying_auth)
            else:
                self.try_register(user_trying_auth)

    def try_login(self, user: User):
        user_from_db = self.db.get_user(user.username)
        if user_from_db and user_from_db.password == user.password:
            self.com.send_message("1")
            return True
        else:
            self.com.send_message("0")
            return False

    def try_register(self, user: User):
        if self.db.add_user(user):
            self.com.send_message("1")
            return True
        else:
            self.com.send_message("0")
            return False

def main():
    com = CommunicatorServer()
    com.start_listening()
    # now wait for login or register







if __name__ == "__main__":
    main()

from CommunicatorServer import CommunicatorServer
from User import User
from DatabaseManager import UsersDataBase


class ServerManager:

    def __init__(self):
        # init socket and start listening on port
        self.com = CommunicatorServer()
        self.com.start_listening()
        # init user database
        self.user_db = UsersDataBase()

        self.main()

    def main(self):
        self.authenticate_user()

    def authenticate_user(self):
        """
        make the login or register process.
        :return: this function will loop forever untill user sends exit, or finishes the auth procces.
        :rtype:
        """
        msg = self.com.recv_message()
        data_list = msg.split(',')

        if data_list[0] != "login" and data_list[0] != "register":  # check for register or login
            self.com.send_message("0")
            self.authenticate_user()

        user_trying_auth = User(data_list[1], data_list[2])

        auth_success = False

        if data_list[0] == "login":
            auth_success = self.try_login(user_trying_auth)
        else:
            auth_success = self.try_register(user_trying_auth)

            if not auth_success:
                self.authenticate_user()

    def try_login(self, user: User):
        user_from_db = self.user_db.get_user(user.username)

        if user_from_db is None:
            self.com.send_message("0")
            return False

        if user_from_db.password == user.password:
            self.com.send_message("1")
            return True

        self.com.send_message("0")
        return False

    def try_register(self, user: User):
        if self.user_db.add_user(user):
            self.com.send_message("1")
            return True
        else:
            self.com.send_message("0")
            return False


def main():
    server_manager = ServerManager()







if __name__ == "__main__":
    main()

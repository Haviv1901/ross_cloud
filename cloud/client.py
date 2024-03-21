from CloudManager import *


class ClientManager:

    def __init__(self):
        self.cloud_manager = CloudManager()
        self.start()

    def start(self):
        self.print_main_menu()
        if self.login_or_register():
            print("Logged in successfully!")
        while True:
            continue

    @staticmethod
    def print_main_menu(self):
        print("--- Welcome to ross cloud ! ---")

    def login_or_register(self):
        print("--- login or register ? (r/l) ---")
        if input() == "r":
            return self.register()
        else:
            return self.login()

    def register(self):
        print("Enter your username:")
        username = input()
        print("Enter your password:")
        password = input()
        if self.cloud_manager.cloud_register(username, password):
            print("Registration successful!")
        else:
            print("Registration failed. Please try again.")
            self.register()

    def login(self):
        print("Enter your username:")
        username = input()
        print("Enter your password:")
        password = input()
        if self.cloud_manager.cloud_login(username, password):
            print("Login successful!")
        else:
            print("Login failed. Please try again.")
            self.login()



def main():
    main_menu = MainMenu()



if __name__ == "__main__":
    main()


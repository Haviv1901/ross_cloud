from CommunicatorServer import *


def main():
    com = CommunicatorServer()
    com.start_listening()
    # now wait for login or register

    while True:
        msg = com.recv_message()
        print(msg)
        com.send_message("1")




if __name__ == "__main__":
    main()

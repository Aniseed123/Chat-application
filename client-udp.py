import socket
import argparse
import select
import sys
import time

server = ("127.0.0.1", 1234)
chat_client_port = 0
is_chat_request = False
target_client_port = ()


def getline():
    i, o, e = select.select([sys.stdin], [], [], 1)
    for s in i:
        if s == sys.stdin:
            input_text = sys.stdin.readline()
            return input_text

    return False


def client_program(user_name):

    global is_chat_request, target_client_port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.setblocking(False)

    signin_msg = "SIGNIN " + user_name
    client_socket.sendto(signin_msg.encode(), server)

    input_msg = "<>"

    while True:

        try:
            server_message, addr = client_socket.recvfrom(2048)
            if server_message:
                print("<FROM " + str(addr) + " > " + str(server_message.decode()))

            if is_chat_request:

                if len(target_client_port) == 0:

                    target_client_port = eval(server_message.decode().replace("server>", ""))
                    print("TARGET CLIENT -> " + str(target_client_port))

        except socket.error:
            pass

        input_msg = getline()
        if input_msg:

            print("<<CLIENT-DEBUG>> " + str(input_msg))

            target_message = input_msg
            client_socket.sendto(target_message.encode(), server)

            if input_msg.lower().startswith("send"):
                is_chat_request = True
                input_msg = input_msg.split(" ")[2]

            if input_msg.lower().strip() == "bye":
                break

            time.sleep(5)
            if len(target_client_port) != 0:
                client_socket.sendto(input_msg.encode(), target_client_port)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", type=str, required=True, help="Username must be specified")
    args = parser.parse_args()

    username = args.username

    client_program(user_name=username)

    print("Client terminated..")
    

import socket

host = "127.0.0.1"
port = 1234

clients_list = {}


def get_connected_clients():
    return " ".join(clients_list.keys())


def get_ip_port_info(username):

    if username in clients_list:
        return clients_list[username]

    return None


def accept_connections(server_socket):

    while True:

        response_message = ""
        address = server_socket.recvfrom(2048)
        message = address[0].decode()
        dest = address[1]
        print("<<DEBUG-SERVER> Message from Client - " + str(dest) + " >" + str(message))

        if message.lower().strip().startswith("signin"):
            response_message = "Welcome to CY6740"
            username = message.split(" ")[1]
            clients_list[username] = dest
        elif message.lower().strip() == "list":
            response_message = get_connected_clients()
        elif message.lower().strip().startswith("send"):
            destination_username = message.split()[1]
            response_message = "server>" + str(get_ip_port_info(destination_username))
        else:
            continue

        server_socket.sendto(response_message.encode(), dest)


def start_server(server_host, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_host, server_port))

    print("Server Initialized... Server is left running ")

    while True:
        accept_connections(server_socket)


if __name__ == "__main__":
    start_server(server_host=host, server_port=port)
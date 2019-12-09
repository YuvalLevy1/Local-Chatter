# Basic server
import socket
import threading
import protocol

IP = '0.0.0.0'  # IP for all available network interfaces in current machine
PORT = 12345
BUFFER = 1024


def get_username_and_message(client_message):
    client_message = str(client_message).split(":")
    username, message = client_message
    message = message.strip()
    return [username, message]


def delete_socket(client_socket, list_of_sockets):
    for socket in list_of_sockets:
        if socket == client_socket:
            list_of_sockets.remove(socket)
    return list_of_sockets


def create_and_send_response(request_str, client_socket, list_of_sockets):
    """Receive the client message as parameter, create
    and return the response according to the protocol.
    Available commands: [Name]/.../[Exit]
    """
    response_str = ""
    username, message = get_username_and_message(request_str)
    # get all letters as lower
    message = message.lower()
    if request_str:  # if request_str != "" and request_str != None. Socket get "" after disconnection

        if message == "exit":
            response_str = username + ": " + "Bye!"
            list_of_sockets = delete_socket(client_socket, list_of_sockets)
            protocol.send_response(client_socket, response_str)
        else:
            response_str = request_str

        username, answer = get_username_and_message(response_str)
        for socket in list_of_sockets:
            if socket is not None and socket != client_socket and answer != "Bye!":
                protocol.send_response(socket, response_str)
    return answer != "Bye!" and message != "exit"


def conversation(client_socket, client_address, list_of_sockets):
    """
    implements the conversation with one client
    """
    ip, port = client_address
    print("Client connected. Client ip  =", ip, ", client port =", port)

    ack = True
    try:
        while ack:
            # create and send the response
            request = protocol.get_request(client_socket)
            username, message = get_username_and_message(request)
            print(f"{username} sent:", message)
            ack = create_and_send_response(request, client_socket, list_of_sockets)
    finally:
        client_socket.close()
    print("Client close the connection. Client ip  =", ip, ", client port =", port)


def main():
    # Set up the server:
    # create an INET, STREAMing socket
    # (IP v4 protocol in Network(Internet) Layer and TCP protocol in Transport Layer)
    # socket.AF_INET, socket.SOCK_STREAM are the default attributes for socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # When you create a socket, you don't really own it. The OS (TCP stack) creates it for you and gives you
    #  a handle (file descriptor) to access it. When your socket is closed, it take time for the OS to "fully close it"
    # socket.SO_REUSEADDR, causes the port to be released immediately after the socket is closed.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind socket to IP and  PORT_NUMBER
    server_socket.bind((IP, PORT))

    # the socket begin to listen for incoming connections.
    # the parameter in number of new connections to hold in queue.
    # Queued connections are ones received, but not yet accepted.
    server_socket.listen(1)
    print("Server is listening.")
    list_of_sockets = []
    try:
        while True:
            # Connection point, server wait for client
            client_socket, client_address = server_socket.accept()
            list_of_sockets.append(client_socket)
            # start conversation with new client in parallel thread
            thread_for_client = threading.Thread(target=conversation,
                                                 args=(client_socket, client_address, list_of_sockets))
            thread_for_client.start()

    finally:
        server_socket.close()


if __name__ == '__main__':
    main()

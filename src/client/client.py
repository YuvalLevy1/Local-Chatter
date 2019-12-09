import socket
import protocol
import threading
import time

end_boolean = False

HOST_IP = "127.0.0.1"
PORT = 12345
BUFFER = 1024


def get_username_and_message(client_message):
    client_message = str(client_message).split(":", maxsplit=1)
    username, message = client_message
    message = message.strip()
    return [username, message]


def get_responses(client_socket):
    global end_boolean
    while True:
        response = protocol.get_response(client_socket)
        username, message = get_username_and_message(response)
        if response and message != "Bye!":
            print(response)
        else:
            if not response:
                print("Server crashes")
            end_boolean = True
            print("ended thread")
            break


def main():
    """implements the conversation with server"""
    # Open client socket, Transport layer: protocol TCP, Network layer: protocol IP
    client_socket = socket.socket()
    client_socket.connect((HOST_IP, PORT))
    # start conversation with new client in parallel thread
    thread_for_responses = threading.Thread(target=get_responses, args=(client_socket,))
    thread_for_responses.start()
    username = input("enter username: ")
    global end_boolean
    try:
        while not end_boolean:
            # Get request from keyboard

            client_request_str = username + ": " + input("")

            if client_request_str:  # if client_request_str not empty string
                # send request according to the protocol
                protocol.send_request(client_socket, client_request_str)
                username, message = get_username_and_message(client_request_str)
                if message == "exit":
                    time.sleep(1)
                    break
        print("disconnected")

    finally:
        client_socket.close()


if __name__ == '__main__':
    main()

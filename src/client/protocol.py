# -*- coding: utf-8 -*-

MESSAGE_LEN = 4


def get_response(client_socket):

    """Receives response from basic_server.server according to the protocol and returns it."""
    len_response_str = client_socket.recv(MESSAGE_LEN)
    # decode by utf-8 standart, convert to string
    len_response_str = len_response_str.decode()
    len_response = int(len_response_str)
    response = client_socket.recv(len_response)
    # remove white chars (TAB, ENTER)
    response = response.strip()
    # decode by utf-8 standart, convert to string
    response_str = response.decode()
    return response_str


def send_request(client_socket, request_str):
    """Send the request according to the protocol.
    """
    # calculate the length of the request and covert it to MESSAGE_LEN length string
    request_len_str = str(len(request_str)).zfill(MESSAGE_LEN)
    request_str = "".join([request_len_str, request_str])
    # convert string to bytes and encode utf-8 standart
    request = request_str.encode()
    client_socket.send(request)
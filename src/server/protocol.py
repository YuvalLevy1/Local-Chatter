# -*- coding: utf-8 -*-

MESSAGE_LEN = 4


def get_request(client_socket):

    """Receive request from basic_server.client according to the protocol and return it."""
    len_request_str = client_socket.recv(MESSAGE_LEN)
    # decode by utf-8 standart, convert to string
    len_request_str = len_request_str.decode()
    len_request = int(len_request_str)
    request = client_socket.recv(len_request)
    # remove white chars (TAB, ENTER)
    request = request.strip()
    # decode by utf-8 standart, convert to string
    request_str = request.decode()
    return request_str


def send_response(client_socket, response_str):
    """Return the response according to the protocol.
    """
    # calculate the length of the response and covert it to MESSAGE_LEN length string
    response_len_str = str(len(response_str)).zfill(MESSAGE_LEN)
    response_str = "".join([response_len_str, response_str])
    # convert string to bytes and encode utf-8 standart
    response = response_str.encode()
    client_socket.send(response)
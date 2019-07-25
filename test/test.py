import socket
from pystreamprotocol import pystream
from threading import Thread

x = b'This is your message'
port = 8000


def receive() -> None:
    """
    Creates a new socket, binds to it, and listens for
    a connection. Upon receiving a connection, the new socket
    is passed to the PysteamProtocol DataReceiver object. From
    there, it begins listening for a Message object. For testing
    purposes, this function should be called first, on a separate
    thread.
    :return: None
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', port))
        sock.listen(2)
        conn, addr = sock.accept()
        receiver = pystream.DataReceiver(conn)
        msg = receiver.receive()
        print(msg)


def send(message: bytearray) -> None:
    """
    Connects to a listening localhost, and sends a message, of type
    bytearray.
    :param message: bytearray object, containing content of message
    :return: None
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', port))
        print("Test: Sending: " + message.decode())
        sender = pystream.DataSender(sock)
        sender.send(message)


listen_thread = Thread(target=receive)
listen_thread.start()

send(x)

import socket
from pystreamprotocol import pystream


x = b'This is your message'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', 6000))
    print("Test: Sending: " + x.decode())
    sender = pystream.DataSender(sock)
    sender.send(x)
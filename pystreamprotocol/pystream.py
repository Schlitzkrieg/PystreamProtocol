import hashlib
from socket import socket

class DataMessage():
    def __init__(self):
        self.message_type = ''
        self.message_length = 0
        self.message_content = None

class DataReceiver():
    def __init__(self, socket, buff_size: int=1024) -> None:
        self.socket = socket
        self.buff_size = buff_size

    def receive(self) -> bytearray:
        package = bytearray()

        if self.socket.recv(2) == b'RS':
            self.socket.send(b'sx')
            msg = self.socket.recv(4)
            buff = int(msg[1:])
            self.socket.send(b'R' + str(buff).zfill(3).encode())
            while len(package) != buff:
                data = self.socket.recv(1)
                if data:
                    package.extend(data)
            recv_hash = hashlib.md5()
            recv_hash.update(package)
            print("DataReceiver(): receive hash: " + str(recv_hash) + ' bytes received: ' + str(package))
            self.socket.send(recv_hash.digest())

        return package


class DataSender():
    def __init__(self, socket: socket) -> None:
        self.socket = socket

    def send(self, bytes_like_obj: bytes) -> None:
        byte_array_hash = hashlib.md5()
        byte_array_hash.update(bytes_like_obj)
        # I am Ready to send
        self.socket.send("RS".encode())
        # if connection replies 'send it'
        if self.socket.recv(2) == b"sx":
            # I am sending n bytes "S" + str(n)
            self.socket.send(("S" + str(len(bytes_like_obj)).zfill(3)).encode())

            if self.socket.recv(4) == ("R" + str(len(bytes_like_obj)).zfill(3)).encode():
                self.socket.send(bytes_like_obj)
                # did you get that?
                # check hash
                client_hash = self.socket.recv(16)

                if client_hash == byte_array_hash.digest():
                    print("DataSender(): Success!")
                else:
                    print(
                        "DataSender(): Failure. Hash received: " + str(byte_array_hash) +
                        ' bytes sent: ' + str(bytes_like_obj)
                    )

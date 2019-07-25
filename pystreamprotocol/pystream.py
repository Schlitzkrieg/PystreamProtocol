import hashlib
from socket import socket


class DataMessage:
    def __init__(self):
        self.message_type = ''
        self.message_length = 0
        self.message_content = None


class DataReceiver:
    def __init__(self, socket, buff_size: int=1024) -> None:
        self.socket = socket
        self.buff_size = buff_size

    def receive(self) -> bytearray:
        """
        Listens for incoming bytes on self.socket. If the first 2 bytes received
        are b'RS' for "Ready to Send," then the bytes b'sx' are sent, to represent
        "Start sending." After sending this, self.socket will receive another 4 bytes.
        These bytes should be lead with a 'S' character, followed by 3 bytes representing
        how long the message is going to be. The variable 'buff' will be an int, created
        from the msg bytes after the 'S' has been removed. Now, the function knows how
        large the buffer should be for the incoming message. The function will send back
        to the sender 4 bytes, starting with 'R' for "Ready to receive," and followed by
        the buffer size.

        After this, the function will accept one byte at a time, appending it to the
        bytearray named 'package.' Once the length of package is the same size as buff,
        and md5 hash of the message will be generated and sent back to the sender so that
        the sender can determine if the message made it in its expected, whole form.

        :return: bytearray
        """
        package = bytearray()

        if self.socket.recv(2) == b'RS':
            self.socket.send(b'sx')
            msg = self.socket.recv(4)
            if msg.decode("utf-8")[0] == 'S':
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


class DataSender:
    def __init__(self, socket: socket) -> None:
        self.socket = socket

    def send(self, bytes_like_obj: bytes) -> None:
        """
        Accepts a message in bytes form and sends it over the socket!

        Function first creates an MD5 hash for the bytes_like_obj. Then, it sends the 'RS' message to
        indicate "Ready to Send." We then wait and listen for the receiver to sen 'sx' for, "Ready to receive."
        Once those bytes are received, we send 'S' followed by a 0 padded 3 char representation of the number
        of bytes our message will be. (Yes, for now, this is limited to 999 chars). At this point, the socket listens
        for an 'R' followed by the same 3 char message length. If it's a match, the whole message is sent, and
        the socket goes back to listening. This time, it's listening for a 16 byte, MD5 hash. If the hash is
        a match, a success message is printed to the console. Else, a failure message showing the hash received
        is printed.

        :param bytes_like_obj:
        :return: None
        """
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

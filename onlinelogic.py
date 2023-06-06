# https://docs.python.org/3/howto/sockets.html
import socket

import gamelogic

clientsocket = None
max_msg_len = 5


class GameSocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        global max_msg_len
        totalsent = 0
        while totalsent < max_msg_len:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                break
            #     raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive(self):
        global max_msg_len
        chunks = []
        bytes_recd = 0
        while bytes_recd < max_msg_len:
            chunk = self.sock.recv(min(max_msg_len - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broke")
            print("check receive")

            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b"".join(chunks)


class serversocket:
    def create_server(self):
        global clientsocket
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        # serversocket.bind((socket.gethostname(), 25565))
        serversocket.bind((socket.gethostname(), 25565))

        print(socket.gethostname())
        # become a server socket
        serversocket.listen(5)

        while True:
            print("Hello")
            # accept connections from outside
            (clientsocket, address) = serversocket.accept()


            print(clientsocket, address)
# https://docs.python.org/3/howto/sockets.html
#Authored by Michael(s214954)
import socket
import sys

import gamelogic
#initial variables
clientsocket = None
max_msg_len = 5
shutdown = False
ip_text = ''
port_text = 7777

#class that contains the functions for the client socket
class GameSocket:

#initializes the socket
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

#connect the soccket to a server
    def connect(self, host, port):
        print(host)
        print(port)
        self.sock.connect((host, port))

#Sends data to the server
    def send(self, msg):
        global max_msg_len
        totalsent = 0
        while totalsent < max_msg_len:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

#Receives data from the server
    def receive(self):
        global max_msg_len
        chunks = []
        bytes_recd = 0
        while bytes_recd < max_msg_len:
            chunk = self.sock.recv(min(max_msg_len - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broke")
            print("chunk {s}: {v}".format(s = len(chunks), v= chunk ))

            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b"".join(chunks)


#class that contains server
class serversocket:
    global shutdown

    #creates/ starts the server and run initial code
    def create_server(self):
        global clientsocket
        global shutdown
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        # serversocket.bind((socket.gethostname(), 25565))
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((socket.gethostname(), port_text))
        print(socket.gethostname())
        # become a server socket
        serversocket.listen(1)

        (clientsocket, address) = serversocket.accept()
        print("Client has connected to server")
        # accept connections from outside
        value = "Ss" + str(gamelogic.board_size)
        while len(value) < max_msg_len:
            value += " "
        clientsocket.send(bytes(value, "utf-8"))
        value = "Sp" + str(gamelogic.default_starting_player)
        while len(value) < max_msg_len:
            value += " "
        clientsocket.send(bytes(value, "utf-8"))


        print(clientsocket, address)

        #Shutsdown the server when no longer active
        while True:
            if shutdown:
                shutdown = False
                sys.exit()



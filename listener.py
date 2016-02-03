import socket
import config

class Rec():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.bind(
            ('', config.UDP_PORT)
        )

    def get_message(self):
        try:
            data, address = self.sock.recvfrom(1024) # buffer size is 1024 bytes TODO : make this bigger?
        except:
            return

        print "received message:", data, "from :", address
        return data


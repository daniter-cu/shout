import socket
import config
import json

class Rec():
    def __init__(self, user_id):
        self.user_id = user_id
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.bind(
            ('', config.UDP_PORT)
        )

    def get_message(self):
        try:
            data, address = self.sock.recvfrom(1024) # buffer size is 1024 bytes TODO : make this bigger?
            obj = json.loads(data)

        except:
            return
        if obj["user_id"] != self.user_id:
            print "received message:", obj["msg"], " from :", obj["user_id"], " address: ", address



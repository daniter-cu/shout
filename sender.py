import socket
import config
import json

class Sender():
    def __init__(self, user_id, blockchain):
        self.user_id = user_id
        self.blockchain = blockchain
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send(self, msg):
        print "trying to send message : ", msg

        json_str = json.dumps({"user_id": self.user_id, "msg": msg})
        self.sock.sendto(json_str, (config.UDP_BROADCAST_IP, config.UDP_PORT))

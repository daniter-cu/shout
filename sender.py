import socket
import config


class Sender():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send(self, msg):
        print "trying to send message : ", msg
        self.sock.sendto(msg, (config.UDP_BROADCAST_IP, config.UDP_PORT))

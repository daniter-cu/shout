import socket

class Sender():
	def __init__(self):
 		self.sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
 		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


 	def send(msg):
		sock.sendto(msg, (self.UDP_IP, self.UDP_PORT))

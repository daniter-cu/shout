import socket
import config

class Rec():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((config.UDP_LISTEN_IP, config.UDP_PORT))


	def getMessage(self):
  		data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes TODO : make this bigger?
  		print "received message:", data, "from :", addr

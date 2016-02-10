from time import time

class Peers():
	def __init__(self):
		# this is a dict of [peer_id] = timestamp
		self.peers = {}

	def has_peer(self, peer_id):
		return peer_id in self.peers

	def add_peer(self, peer_id):
		self.peers[peer_id] = time()

	def purge_peers(self):
		for peer, timestamp in self.peers.items():
			if time() - timestamp > 3:
				del self.peers[peer]


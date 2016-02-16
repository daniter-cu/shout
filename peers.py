from time import time

class Peers():
    def __init__(self):
        # this is a dict of [peer_id] = timestamp
        self.peers = {}

    def has_peer(self, peer_id):
        return peer_id in self.peers

    def add_peer(self, peer_id, block=None):
        self.peers[peer_id] = (time(), block)

    def purge_peers(self):
        for peer, timestamp, block in self.peers.items():
            if time() - timestamp > 3:
                del self.peers[peer]

    def size(self):
        return len(self.peers)

    def get_consensus(self, current_hash):
        c = {}
        full_set = {}
        for peer, (_, block) in self.peers.items():
            if block and (block.prior_hash == current_hash or current_hash == None):
                h = block.hash()
                full_set[h] = block
                if h in c:
                    c[h]+=1
                else:
                    c[h]=1

        for h, count in c.items():
            if count > self.size()/2:
                return full_set[h]

        return None

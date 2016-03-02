from time import time

class Peers():
    def __init__(self, sender):
        # this is a dict of [peer_id] = timestamp
        self.peers = {}
        self.sender = sender

    def __str__(self):
        return str(self.peers)

    def has_peer(self, peer_id):
        return peer_id in self.peers

    def add_peer(self, peer_id, last_hash, block=None):
        self.peers[peer_id] = (time(), last_hash, block)

    def purge_peers(self):
        for peer, (timestamp, _last_hash, _block) in self.peers.items():
            if time() - timestamp > 3:
                del self.peers[peer]

    def size(self):
        return len(self.peers)

    def get_consensus(self):

        block_set = {}
        block_count = {}
        hash_count = {}
        for peer, (_, last_hash, block) in self.peers.items():
            if block:
                hash = block.hash()
                block_set[hash] = block
                block_count[hash] = block_count[hash] + 1 if hash in block_count else 1

            hash_count[last_hash] = hash_count[last_hash] + 1 if last_hash in hash_count else 1

        last_hash = None
        block = None
        for hash, count in block_count.items():
            if count > self.size()/2:
                block = block_set[hash]
        for hash, count in hash_count.items():
            if count >= self.size()/2:  # I think we need to let ties win in this situation.
                last_hash = hash

        return last_hash, block
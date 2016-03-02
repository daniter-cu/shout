import socket
import config
import json
from block import *
import logging
from block_type import *

logger = logging.getLogger()

class Rec():
    def __init__(self, user_id, blockchain, peers_list, client, sender):
        self.client = client
        self.peers_list = peers_list
        self.user_id = user_id
        self.blockchain = blockchain

        self.patchRequests = {}

        self.sender = sender
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
        
        if "user_id" in obj :
            if obj["block_type"] == BlockType.heartbeat:
                #logger.info("%s - Recieved HEARTBEAT: %s" % (self.user_id, data))
                if obj["proposed_block"]:
                    # TODO : put this into block class
                    pb = obj["proposed_block"]
                    block = Block(pb["block_type"], pb["user_id"], pb["prior_hash"], pb["payload"])
                    self.peers_list.add_peer(obj["user_id"], obj["prior_hash"], block)
                else: # this is the vanilla heartbeat case
                    self.peers_list.add_peer(obj["user_id"], obj["prior_hash"])
            if obj["block_type"] == BlockType.message and obj["user_id"] != self.user_id :
                # TODO : Don't over write if you're waiting for a message to get accepted
                if self.blockchain.proposal_allowed():
                    logger.info("%s - Received MESSAGE: %s" % (self.user_id, data))
                    last_hash = None
                    if not self.blockchain.is_empty():
                        last_hash = self.blockchain.peek().hash()

                    if not last_hash or last_hash == obj["prior_hash"] or obj["prior_hash"] == "":
                        block = Block(BlockType.message, obj["user_id"], obj["prior_hash"], obj["payload"])
                        self.blockchain.propose_block(block)    
            if obj["block_type"] == BlockType.requestHistory:
                # Someone is requesting the history so be a nice person and send it
                self.sender.send_history(obj["payload"]["hash"])

            if obj["block_type"] == BlockType.sendHistory:
                # Some nice person sent a history of the blockchain
                block = Block(BlockType.message, obj["user_id"], obj["prior_hash"], obj["payload"])
                if block.hash() in self.patchRequests:
                    del self.patchRequests[block.hash()]
                    self.blockchain.patch(block)

        self.run_consensus()
        self.client.update()
        self.repair()

    def run_consensus(self):
        self.peers_list.purge_peers()

        (last_hash, block) = self.peers_list.get_consensus()
        self.blockchain.verify_last_hash(last_hash)

        if block:
            # Always accept the group consensus
            self.blockchain.accept_proposed_block(block)

    def repair(self):
        for nsync in self.blockchain.get_all_nsyncs():
            _hash = nsync.hash()
            self.patchRequests[_hash] = self.patchRequests[_hash] + 1 if _hash in self.patchRequests else 1
            if self.patchRequests[_hash] < 5: # Limit number of times you can request a block
                self.sender.request_history(_hash)

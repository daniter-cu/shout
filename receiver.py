import socket
import config
import json
from block import *

class Rec():
    def __init__(self, user_id, blockchain, peers_list):
        self.peers_list = peers_list
        self.user_id = user_id
        self.blockchain = blockchain
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
        
        # print obj

        if "user_id" in obj and obj["user_id"] != self.user_id:
            #print "received message:", obj["msg"], " from :", obj["user_id"], " address: ", address
            if obj["proposed_block"]:
                # TODO : put this into block class
                pb = obj["proposed_block"]
                block = Block(pb["block_type"], pb["creator_id"], pb["prior_hash"], pb["payload"], pb["salt"])
                self.peers_list.add_peer(obj["user_id"], block)
            else: # this is the vanilla heartbeat case
                self.peers_list.add_peer(obj["user_id"])
            #self.peers_list.peers
            #TODO : purge peers
        prev_block = self.blockchain.peek()
        if prev_block:
            prev_hash = prev_block.hash()
        else:
            prev_hash = None
        block = self.peers_list.get_consensus(prev_hash)
        if block:
            self.blockchain.push(block)


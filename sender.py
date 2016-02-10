import socket
import config
import json
from block import *
from block_type import *
from heartbeat import *

class Sender():
    def __init__(self, user_id, blockchain):
        self.user_id = user_id
        self.blockchain = blockchain
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send(self, msg):
        print "Trying to send message : ", msg

        if self.blockchain.is_next_block_proposed():
            print "Blockchain currently pending approval."
        else:

            last_hash = ""
            if not self.blockchain.is_empty():
                last_hash = self.blockchain.peek().hash()

            block = Block(BlockType.message, self.user_id, last_hash, msg)
            self.blockchain.propose_block(block)

    def heartbeat(self):
        last_block = self.blockchain.peek()
        proposed_block = self.blockchain.proposedBlock
        heartbeat = Heartbeat(last_block, proposed_block)

        self.sock.sendto(heartbeat.to_json, (config.UDP_BROADCAST_IP, config.UDP_PORT))
import socket
import config
from block import *
from block_type import *
from heartbeat import *
import threading
import logging


logger = logging.getLogger()

class Sender():
    def __init__(self, user_id, blockchain):
        self.user_id = user_id
        self.blockchain = blockchain
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.heartbeat_interval = config.HEARTBEAT_INTERVAL
        self.heartbeat()

    def send(self, block):
        self.blockchain.propose_block(block)
        self.__send(block.to_json())

    def heartbeat(self):
        last_block = self.blockchain.peek()
        proposed_block = self.blockchain.proposedBlock
        heartbeat = Heartbeat(self.user_id, last_block, proposed_block)

        self.__send(heartbeat.to_json())

        t = threading.Timer(self.heartbeat_interval, self.heartbeat)
        t.setDaemon(True)
        t.start()

    def request_history(self, request_hash):
        payload = {"hash": request_hash}
        block = Block(BlockType.requestHistory, self.user_id, "", payload)
        self.__send(block.to_json())

    def send_history(self, request_hash):
        block = self.blockchain.get_by_hash(request_hash)
        if block and block.block_type != BlockType.nSync:
            h_block = Block(BlockType.sendHistory, block.creator_id, block.prior_hash, block.payload)
            self.__send(h_block.to_json())

    def __send(self, data):
        logger.info("Sending: " + data)
        self.sock.sendto(data, (config.UDP_BROADCAST_IP, config.UDP_PORT))
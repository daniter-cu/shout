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

    def request_history(self, _hash):
        payload = {"hash": _hash, "count": 10}
        block = Block(BlockType.requestHistory, self.user_id, None, payload)
        self.__send(block.to_json())

    def send_history(self, hash, count):

        blocks = self.blockchain.getHistory(hash, count)
        if blocks is not None:
            _json = map(lambda b: b.to_json, blocks)
            block = Block(BlockType.sendHistory, self.user_id, None, _json)
            self.__send(block.to_json())

    def __send(self, data):
        logger.info("Sending: " + data)
        self.sock.sendto(data, (config.UDP_BROADCAST_IP, config.UDP_PORT))
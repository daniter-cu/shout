import socket
import config
import json
from block import *
from block_type import *
from heartbeat import *
import threading
import logging
import time
import random

logger = logging.getLogger()

class Sender():
    def __init__(self, user_id, blockchain):
        self.user_id = user_id
        self.blockchain = blockchain
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.heartbeat_interval = 1
        self.resend_timeout = 2
        self.heartbeat()



    # def send(self, msg):
    #     # print "Trying to send message: ", msg
    #     last_hash = ""
    #     if not self.blockchain.is_empty():
    #         last_hash = self.blockchain.peek().hash()

    #     block = Block(BlockType.message, self.user_id, last_hash, msg)
    #     self.blockchain.propose_block(block)

    #     json = block.to_json()
    #     logger.info("Sending: "+ json)
    #     self.sock.sendto(json, (config.UDP_BROADCAST_IP, config.UDP_PORT))
    #     t = threading.Timer(self.resend_timeout, self.resend, [msg, block.hash()])
    #     t.setDaemon(True)
    #     t.start()

    def send(self, block):
        self.blockchain.propose_block(block)
        json = block.to_json()
        logger.info("Sending: "+ json)
        self.sock.sendto(json, (config.UDP_BROADCAST_IP, config.UDP_PORT))


    def resend(self, message, hash):
        if self.blockchain.contains(hash):
            logger.info("#### Not resending")
            return
        time.sleep(random.random())
        self.send(message)

    def heartbeat(self):
        last_block = self.blockchain.peek()
        proposed_block = self.blockchain.proposedBlock
        heartbeat = Heartbeat(self.user_id, last_block, proposed_block)

        json = heartbeat.to_json()
        self.sock.sendto(json, (config.UDP_BROADCAST_IP, config.UDP_PORT))

        # TODO : Since we never join on these what happens to the object?
        # Is there a memory leak here?
        t = threading.Timer(self.heartbeat_interval, self.heartbeat)
        t.setDaemon(True)
        t.start()

    def sendQuery(self, hash, count):
        payload = {"hash": hash, "count":count}
        block = Block(BlockType.query, self.user_id, None, payload)
        json = block.to_json()
        self.sock.sendto(json, (config.UDP_BROADCAST_IP, config.UDP_PORT))

    def sendQueryResult(self, res):
        block = Block(BlockType.query_res, self.user_id, None, res)
        json = block.to_json()
        self.sock.sendto(json, (config.UDP_BROADCAST_IP, config.UDP_PORT))
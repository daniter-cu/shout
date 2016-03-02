import time
import logging
from block import *
from block_type import *
import random
from config import *

logger = logging.getLogger()


class MessageQueue():
    def __init__(self, blockchain, sender, user_id):
        self.queue = []
        self.blockchain = blockchain
        self.sender = sender
        self.user_id = user_id

    def add_message(self, msg):
        self.queue.append(msg)

    def consume(self):
        while True:
            if not self.queue:
                time.sleep(EMPTY_QUEUE_TIMEOUT)
            elif self.blockchain.proposal_allowed():
                msg = self.queue.pop(0)
                while True:
                    last_hash = self.blockchain.peek().hash()
                    # if self.blockchain.peek().block_type == BlockType.empty:
                    #     last_hash = ""
                    block = Block(BlockType.message, self.user_id, last_hash, msg)
                    self.sender.send(block)
                    time.sleep(RESEND_TIMEOUT + random.random() * RESEND_RANDOM_FACTOR)
                    if self.blockchain.contains(block.hash()):
                        break
            else:  # we have a message we want to send but htere is a proposal pending
                logger.info("not allowed")
                time.sleep(PROPOSAL_PENDING_TIMEOUT)




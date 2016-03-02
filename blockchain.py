from time import time
import logging
import threading
from block_type import *
from block      import *
from config import *

logger = logging.getLogger()

class Blockchain:
    def __init__(self):
        self.history = []
        self.items = []
        self.proposedBlock = None
        self.timestamp = time()
        self.proposed_timeout = PROPOSAL_TIMEOUT

        # push an empty block so the blockchain is never empty
        self.__push(Block(BlockType.empty, "", "", ""))

    def proposal_allowed(self):
        return self.proposedBlock is None

    def propose_block(self, block):
        self.proposedBlock = block
        t = threading.Timer(self.proposed_timeout, self.clear_proposed)
        t.setDaemon(True)
        t.start()

    def clear_proposed(self):
        self.proposedBlock = None

    def accept_proposed_block(self, block):
        # Note that you might be compelled to just use the self.proposedBlock
        # but this is not always the correct block

        if block.hash() == self.peek().hash(): # Synced correctly
            self.__push(block)
        else:                                  # Out of sync. Create a new block chain
            self.history.push(self.items)
            self.items = [block]
        self.clear_proposed()


    def is_next_block_proposed(self):
        return self.proposedBlock is not None

    def is_empty(self):
        return self.items == []

    def __push(self, item):
        self.items.append(item)

    def __pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[self.size()-1]

    def size(self):
        return len(self.items)

    def get_history(self, _hash, count):
        hashes = map(lambda b: b.hash(), self.items)
        if _hash in hashes:
            index = hashes.index(_hash)
            return self.items[index: -count]

        return None

    # def query(self, hash, count):
    #     index = None
    #     for i, item in enumerate(self.items):
    #         if item.hash() == hash:
    #             index = i
    #             break
    #     if index == None:
    #         return None
    #     else:
    #         if count > 0:
    #             return self.items[i, i+count]
    #         else:
    #             return self.items[i+count, i]

    def update(self, chain):
        if chain[0].prior_hash != self.items.peek().hash:
            logger.error("Update failed with non matching hashes")
        else:
            self.items.extend(chain)

    def __str__(self):
        chain =  "~".join([item.to_json() for item in self.items])
        if self.proposedBlock:
            chain += "->" + self.proposedBlock.to_json()
        return chain

    def contains(self, hash):
        for item in self.items:
            if hash == item.hash():
                return True
        return False







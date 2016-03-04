from time import time
import logging
import threading
from block_type import *
from block      import *
from config import *
from nsync_block import NSyncBlock

logger = logging.getLogger()

class Blockchain:
    def __init__(self):
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

        top_hash = self.peek().hash()
        if block.prior_hash == top_hash:
            self.__push(block)
            logger.info("ACCEPT:" + block.creator_id + " accepts block " + block.payload)
        elif not self.contains(block.hash()):
            # We missed something... push an NSync block
            self.__push(NSyncBlock(block.prior_hash, top_hash))
            self.__push(block)
            logger.info("ACCEPT (with nsync):" + block.creator_id + " accepts block " + block.payload)

    def verify_last_hash(self, last_hash):
        # TODO: contains might be too strong...
        if last_hash is not None and not self.contains(last_hash):
            # We missed something... push an NSync block
            self.__push(NSyncBlock(last_hash, self.peek().hash()))

    def patch(self, block):
        nsync = self.get_by_hash(block.hash())
        if nsync is not None and nsync.block_type == BlockType.nSync:
            index = self.items.index(nsync)
            nsync._hash = block.prior_hash
            if nsync.hash() == nsync.prior_hash: # We have all the missing pieces
                self.items[index] = block
            else:
                self.items.insert(index + 1, block)

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


    def update(self, chain):
        if chain[0].prior_hash != self.items.peek().hash:
            logger.error("Update failed with non matching hashes")
        else:
            self.items.extend(chain)

    def __str__(self):
        chain = "~".join([item.to_json() for item in self.items])
        if self.proposedBlock:
            chain += "->" + self.proposedBlock.to_json()
        return chain

    def contains(self, hash):
        return self.get_by_hash(hash) is not None

    def get_by_hash(self, _hash):
        for item in self.items:
            if _hash == item.hash():
                return item
        return None

    def get_all_nsyncs(self):
        return filter(lambda b: b.block_type == BlockType.nSync, self.items)





from time import time
import logging

logger = logging.getLogger()

class Blockchain:
    def __init__(self):
        self.items = []
        self.proposedBlock = None
        self.timestamp = time()

    def proposal_allowed(self):
        if self.proposedBlock is None:
            return True # no proposed block
        if not self.is_empty() and self.proposedBlock.hash() == self.peek().hash():
            return True # accepted block
        if time() - self.timestamp > 3: # 3 second timeout
            return True
        return False

    def propose_block(self, block):
        self.proposedBlock = block

    def accept_proposed_block(self, block):
        # Note that you might be compeled to just use the self.proposedBlock
        # but htis is not always the correct block
        self.__push(block)

        #self.proposedBlock = None

    def is_next_block_proposed(self):
        return self.proposedBlock is not None

    def is_empty(self):
        return self.items == []

    def __push(self, item):
        self.items.append(item)

    def __pop(self):
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def query(self, hash, count):
        index = None
        for i, item in enumerate(self.items):
            if item.hash() == hash:
                index = i
                break
        if index == None:
            return None
        else:
            if count > 0:
                return self.items[i, i+count]
            else:
                return self.items[i+count, i]

    def update(self, chain):
        if chain[0].prior_hash != self.items.peek().hash:
            logger.error("Update failed with non matching hashes")
        else:
            self.items.extend(chain)

    def __str__(self):
        chain =  "~".join([item.to_json() for item in self.items])
        chain += "->" + self.proposedBlock.to_json()
        return chain







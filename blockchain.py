class Blockchain:
    def __init__(self):
        self.items = []
        self.proposedBlock = None


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
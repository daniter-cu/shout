class Blockchain:
    def __init__(self):
        self.items = []
        self.proposedBlock = None

    # TODO: This might need to remember hashes that failed so it doesn't pick up an old hash from stragglers and try to
    # reach consensus again.

    def propose_block(self, block):
        if self.proposedBlock is not None:
            print "Error: Tried to propose a second block"
        else:
            self.proposedBlock = block

    def is_next_block_proposed(self):
        return self.proposedBlock is not None

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def __pop(self):
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
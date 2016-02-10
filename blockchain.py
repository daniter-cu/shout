class Blockchain:
    def __init__(self):
        self.items = []
        self.proposedBlock = None

    def prior_hash(self):
        if self.is_empty() is True:
            return ""
        return self.__peek().hash()

    def is_next_block_proposed(self):
        return self.proposedBlock is not None

    def is_empty(self):
        return self.items == []

    def __push(self, item):
        self.items.append(item)

    def __pop(self):
        return self.items.pop()

    def __peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
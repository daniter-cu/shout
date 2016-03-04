from block import *
from block_type import *

class NSyncBlock(Block):
    def __init__(self, _hash, prior_hash):
        Block.__init__(self, BlockType.nSync, " ", prior_hash, "")
        self.maxRequests = 50
        self.blocksRequested = 0
        self._hash = _hash

    def hash(self):
        return self._hash
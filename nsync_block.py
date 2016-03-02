from block import *
from block_type import *

class NSyncBlock(Block):
    def __init__(self, _hash, prior_hash):
        Block.__init__(self, BlockType.nSync, prior_hash, "")
        self._hash = _hash

    def __hash__(self):
        return self._hash
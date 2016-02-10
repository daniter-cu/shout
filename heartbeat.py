import json

class Heartbeat:
    def __init__(self, last_block, proposed_block):
        self.items = []
        self.last_block = last_block
        self.proposed_block = proposed_block

    def to_json(self):

        prior_hash = ""
        if self.last_block is not None:
            prior_hash = self.last_block.hash()

        block_json = ""
        if self.proposed_block is not None:
            block_json = json.loads(self.proposed_block.to_json())


        return json.dumps({
            "prior_hash": prior_hash,
            "proposed_block": block_json,
        })
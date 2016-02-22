import json
import uuid
import hashlib

class Block():

    def __init__(self, block_type, creator_id, prior_hash, payload):
        self.block_type = block_type
        self.creator_id = creator_id
        self.prior_hash = prior_hash
        self.payload = payload # TODO: There might be a better name for this. This is the message or chat room name, ect...

    def to_json(self):
        return json.dumps({
            "block_type": self.block_type,
            "user_id": self.creator_id,
            "prior_hash": self.prior_hash,
            "payload": self.payload
        })

    def hash(self):
        str = ''.join([self.creator_id, self.prior_hash, self.payload, self.block_type])
        return hashlib.sha256(str).hexdigest()


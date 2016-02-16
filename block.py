import json
import uuid
import hashlib

class Block():

    def __init__(self, block_type, creator_id, prior_hash, payload, salt=uuid.uuid4().hex):
        self.block_type = block_type
        self.creator_id = creator_id
        self.prior_hash = prior_hash
        self.payload = payload # TODO: There might be a better name for this. This is the message or chat room name, ect...
        self.salt = salt

    def to_json(self):
        return json.dumps({
            "block_type": self.block_type,
            "user_id": self.creator_id,
            "prior_hash": self.prior_hash,
            "payload": self.payload,
            "salt": self.salt
        })

    def hash(self):
        str = ''.join([self.creator_id, self.prior_hash, self.payload, self.salt, self.block_type])
        return hashlib.sha256(str).hexdigest()


class BlockType(object):
    message 	= "msg:"
    ping        = "ping:"
    renameChat  = "room:"
    renameUser  = "name:"
    help        = "help"

    def values(self):
        return {value for key, value in self.__dict__ if not key.startswith('__') and not callable(key)}
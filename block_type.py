class BlockType(object):
    message 	= "MSG"
    ping        = "PING"
    renameChat  = "ROOM"
    renameUser  = "NAME"
    help        = "help"
    heartbeat   = "HEARTBEAT"
    query       = "QUERY"
    query_res   = "RESULT"
    empty       = "EMPTY"

    def values(self):
        return {value for key, value in self.__dict__ if not key.startswith('__') and not callable(key)}
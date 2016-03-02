class BlockType(object):
    message 	   = "MSG"
    ping           = "PING"
    renameChat     = "ROOM"
    renameUser     = "NAME"
    help           = "help"
    heartbeat      = "HEARTBEAT"
    requestHistory = "REQUEST_HISTORY"
    sendHistory    = "SEND_HISTORY"
    empty          = "EMPTY"
    nSync          = "NSYNC"

    def values(self):
        return {value for key, value in self.__dict__ if not key.startswith('__') and not callable(key)}
#!/bin/bash python
from listener import *
from sender import *
from sys import stdin
import re
import threading
import time


class BroadcastType(object):
    message 	= "msg:"
    ping        = "ping:"
    renameChat  = "room:"
    renameUser  = "name:"
    help        = "help"

    def values(self):
        return {value for key, value in self.__dict__ if not key.startswith('__') and not callable(key)}


def get_messages(rec):
    while (True):
        in_msg = rec.get_message()
        print in_msg


def send_message(sender, str):
    sender.send(str.strip())


def rename_chat(sender, str):
    sender.send("Rename chat")


def rename_user(sender, str):
    sender.send("Rename user")


def display_help():
    print """********************** List of Shout commands **********************
msg: Hello, World. 		 # Send a message to the chat room
ping:		 		 # Ping to discover if a room exists.
rename: Hotel California 	 # Rename the chat room.
name: Batman 			 # Change your name.
help 				 # Display a list of commands.
    """


if __name__ == '__main__':
    sender = Sender()
    rec = Rec()

    t = threading.Thread(target=get_messages, args=(rec,))
    t.setDaemon(True)
    t.start()

    while(True):
        senderInput = stdin.readline()


        # ToDo: I'd like to pull this directly from the BroadcastType object
        broadcastValues = "|".join(("msg:", "ping:", "room:", "name:", "help"))

        p = re.compile("^({0})".format(broadcastValues))
        match = re.search(p, senderInput)

        action = BroadcastType.message
        if(match != None):
            action = match.group(0)

        if action == BroadcastType.message:
            send_message(sender, senderInput)
        elif action == BroadcastType.ping:
            sender.send(BroadcastType.ping)
        elif action == BroadcastType.renameChat:
            rename_chat(sender, senderInput)
        elif action == BroadcastType.renameUser:
            rename_user(sender, senderInput)
        elif action == BroadcastType.help:
            display_help()
        else:
            send_message(sender, senderInput)


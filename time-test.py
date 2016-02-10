#!/bin/bash python
from block_type import *
from receiver import *
from sender import *
from sys import stdin
import re
import threading
import time
from uuid import getnode as get_mac
import uuid



def get_messages(rec):
    while (True):
        in_msg = rec.get_message()
        # print in_msg


def send_message(sender, message):
    sender.send(message.strip())


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
    # http://stackoverflow.com/questions/159137/getting-mac-address
    # user_id = get_mac()  # 48-bit number used to identify the user
    user_id = str(uuid.uuid1())

    sender = Sender(user_id)
    rec = Rec(user_id)

    t = threading.Thread(target=get_messages, args=(rec,))
    t.setDaemon(True)
    t.start()


    num = range(1,100)
    i = 0
    while(True):
        #time.sleep(3)
        senderInput = str(num[i])
        i += 1
        if i > 99:
            time.sleep(30)

        # ToDo: I'd like to pull this directly from the BroadcastType object
        broadcastValues = "|".join(("msg:", "ping:", "room:", "name:", "help"))

        p = re.compile("^({0})".format(broadcastValues))
        match = re.search(p, senderInput)

        action = BlockType.message
        if(match != None):
            action = match.group(0)

        if action == BlockType.message:
            send_message(sender, senderInput)
        elif action == BlockType.ping:
            sender.send(BlockType.ping)
        elif action == BlockType.renameChat:
            rename_chat(sender, senderInput)
        elif action == BlockType.renameUser:
            rename_user(sender, senderInput)
        elif action == BlockType.help:
            display_help()
        else:
            send_message(sender, senderInput)


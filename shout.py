#!/bin/bash python
from blockchain import *
from block_type import *
from receiver import *
from sender import *
from peers import *
from sys import stdin
import re
import threading
import time
from uuid import getnode as get_mac
import uuid
from subprocess import call, STDOUT
import os
from client import *
import logging
from msgq import *



def get_messages(rec):
    while (True):
        in_msg = rec.get_message()
        # print in_msg

def start_permisc_mode():
    FNULL = open(os.devnull, 'w')
    call(['tcpdump', '-Ii', 'en0'], stdout=FNULL, stderr=STDOUT)



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
    logging.basicConfig(filename='shout.log', level=logging.INFO)

    user_id = str(uuid.uuid1())

    blockchain = Blockchain()

    sender = Sender(user_id, blockchain, start_permisc_mode)
    peers_list = Peers(sender)
    msgq = MessageQueue(blockchain, sender, user_id)
    client = ClientWindow(blockchain, peers_list, msgq)
    rec = Rec(user_id, blockchain, peers_list, client, sender)

    t = threading.Thread(target=msgq.consume)
    t.setDaemon(True)
    t.start()

    t = threading.Thread(target=get_messages, args=(rec,))
    t.setDaemon(True)
    t.start()

    t = threading.Thread(target=start_permisc_mode)
    t.setDaemon(True)
    t.start()

    client.start()


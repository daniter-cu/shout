#!/bin/bash python
from listener import *
from sender import *
from sys import stdin
import threading
import time

def getMessages(rec):
	while (True):
		in_msg = rec.getMessage()
		print in_msg


if __name__=='__main__':
	sender = Sender()
	rec = Rec()

	t = threading.Thread(target=getMessages, args=(rec,))
	t.setDaemon(True)
	t.start()

	while(True):
		out_msg = stdin.readline()
		sender.send(out_msg.strip())
#!/bin/bash python
from listener import *
from sender import *

if __name__=='__main__':
	sender = Sender()
	rec = Rec()

	while(True):
		in_msg = rec.getMessage()
		if in_msg:
			print in_msg
		out_msg = raw_input()
		sender.send(out_msg)
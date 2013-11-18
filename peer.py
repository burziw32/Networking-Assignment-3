'''
peer.py
Jason Blackwell
Walter Burzik
11/18/2013
'''
import os, sys
from socket import *

        
peername = str(sys.argv[1])
myIP = str(sys.argv[2])
myPort = str(sys.argv[3])
pathToDirectory = str(sys.argv[4])
peerIP = str(sys.argv[5])
peerPort = str(sys.argv[6])

if (len(sys.argv) < 4 or len(sys.argv) = 5 or len(sys.argv) > 6):
    print "incorrect number of argv"
elif (len(sys.argv) == 4):
    print "First peer"
elif (len(sys.argv)== 6):
    print "Peer"
else:
    print "Error"


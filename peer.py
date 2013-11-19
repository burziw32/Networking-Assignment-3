'''
peer.py
Jason Blackwell
Walter Burzik
11/18/2013
'''
import os, sys
from socket import *
import threading

class UDPServer (threading.Thread):
    def __init__(self, threadID,serverPort):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.serverPort = serverPort
        self.counter = 0
        self.done = False
        
    def run(self):
        print "Starting UDP server thread"
	serverSocket = socket(AF_INET,SOCK_DGRAM)
	serverSocket.bind(('',self.serverPort))
	print "The UDP server is ready to receive"
	while not(self.done):
		mesg, clientAddress = serverSocket.recvfrom(2048)
		self.counter +=1
		modifiedMesg = mesg.upper()
		serverSocket.sendto(modifiedMesg,clientAddress)

        print "Exiting UDP server thread"


class TCPServer (threading.Thread):
    def __init__(self, threadID,serverPort):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.serverPort = serverPort
        self.counter = 0
        self.done = False
        
    def run(self):
        print "Starting TCP server thread"
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',self.serverPort))
	serverSocket.listen(5)
	print "The TCP server is ready to receive"
	while not(self.done):
		connectionSocket,addr = serverSocket.accept()
		self.counter +=1
		mesg= connectionSocket.recv(2048)
		modifiedMesg = mesg[::-1]
		connectionSocket.send(modifiedMesg)
		connectionSocket.close()        

        print "Exiting TCP server thread"

        
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


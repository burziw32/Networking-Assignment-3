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
    def __init__(self, threadID,lookupPort):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.lookupPort = lookupPort
        self.counter = 0
        self.done = False
        
    def run(self):
        print "Starting UDP server thread"
	serverSocket = socket(AF_INET,SOCK_DGRAM)
	serverSocket.bind(('',self.lookupPort))
	print "The UDP server is ready to receive"
	while not(self.done):
		mesg, clientAddress = serverSocket.recvfrom(2048)
		self.counter +=1
		modifiedMesg = mesg.upper()
		serverSocket.sendto(modifiedMesg,clientAddress)

        print "Exiting UDP server thread"


class TCPServer (threading.Thread):
    def __init__(self, threadID,fileTransferPort):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.fileTransferPort = fileTransferPort
        self.counter = 0
        self.done = False
        
    def run(self):
        print "Starting TCP server thread"
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',self.fileTransferPort))
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

        
if (len(sys.argv) < 5 or len(sys.argv) == 6 or len(sys.argv) > 7):
    sys.exit("incorrect number of args \n peer.py [PEER NAME] [MY IP] [MY PORT] [PATH TO DIRECTORY] [optional PEER IP] [optional PEER PORT]")
elif (len(sys.argv) == 5):
    print "First peer"
elif (len(sys.argv) == 7):
    print "Peer"
else:
    sys.exit("Error message")

peername = sys.argv[1]
myIP = sys.argv[2]
myPort = sys.argv[3]
pathToDirectory = sys.argv[4]
# peerIP = sys.argv[5]
# peerPort = sys.argv[6]

print "Peer Name: " + peername
print "My IP: " + myIP
print "My Port: " + myPort
print "Directory: " + pathToDirectory
udpPort = myPort
tcpPort = int(myPort) + 1 
print "TCP Port: " + str(tcpPort)
print "UDP Port: " + udpPort
# print peerIP
# print peerPort

def runTCPClient(str,tcp):
	clientSocket = socket(AF_INET,SOCK_STREAM)
	clientSocket.connect(("localhost",tcp))
	clientSocket.send(str)
	modifiedMesg,serverAddress = clientSocket.recvfrom(2048)
	clientSocket.close()
	return modifiedMesg
	
def runUDPClient(str, udp):
	clientSocket = socket(AF_INET,SOCK_DGRAM)	
	clientSocket.sendto(str,("localhost",udp))
	modifiedMesg,serverAddress = clientSocket.recvfrom(2048)
	return modifiedMesg

#Main Thread
#counter=0
#tcpPort=12000
#udpPort=13000

# Create new threads
#thread1 = TCPServer(1,tcpPort)
#thread2 = UDPServer(2,udpPort)


# Start new Threads
#thread1.start()
#thread2.start()

#choice =""
#while choice !="Q":
#	choice = raw_input("Choose an option-->[S]tatus, [E]cho, [U]ppercase, [R]everse, [Q]uit: ")
#	if (choice=="S"):
#		print "\tTCP server has served",thread1.counter,"clients"
#		print "\tUDP server has served",thread2.counter,"clients"
#		print "\tMain Thread has served",counter,"clients"
#	if (choice=="E"):
#		str = raw_input("\tEnter a string to be echoed: ");
#		counter += 1
#		print "\tEchoed string is ",str
#	if (choice=="U"):
#		str = raw_input("\tEnter a string to be made uppercase: ");
#		mesg = runUDPClient(str,udpPort)
#		print "\tUppercase string is ",mesg
#	if (choice=="R"):
#		str = raw_input("\tEnter a string to be reversed: ");
#		mesg = runTCPClient(str,tcpPort)
#		print "\tReversed string is ",mesg


#Send stop message to threads	
#thread1.done=True
#thread2.done=True

#if blocking in thread1 and thread2, you can send "pings" from here to both those ports to force them out of blocking and check the loop condition
#runTCPClient("quit",tcpPort)
#runUDPClient("quit",udpPort)

#print "Waiting for all threads to complete"
#thread1.join()
#thread2.join()

#print "Exiting Main Thread"

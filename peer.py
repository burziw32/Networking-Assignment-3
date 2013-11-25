'''
peer.py
Jason Blackwell
Walter Burzik
11/24/2013
'''
import os, sys
from socket import *
import threading
import select
from os import walk

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
		print "Request"
		if "add" in mesg:
			print "Peer Requesting Add"
			print clientAddress
			print mesg
			newPeer = mesg.split()
			neighbors.append(newPeer[1])
			neighbors.append(newPeer[2])
			neighbors.append(newPeer[3])
			modifiedMesg = "accept"
			serverSocket.sendto(modifiedMesg,clientAddress)
		if "find" in mesg:
			print "Peer Requesting Find"
			print clientAddress
			print mesg
			daMessage = mesg.split()
			daFile = daMessage[1]
			daPeerIP = daMessage[3]
			daPeerPort = daMessage[4]
			print "finding: " + daFile
			if daFile in files:
				print "you have the file: " + daFile
				openUDPClient("found " + daFile + " " + myIP + " " + str(tcpPort), daPeerIP, int(daPeerPort))
			else:
				for counter in xrange(0,len(neighbors),3):
					print openUDPClient("find " + daFile + " " + peername + " "+ daPeerIP + " " + str(daPeerPort) + " " + str(seqNbr), neighbors[1], int(neighbors[2]))
				seqNbr += 1
		if "found" in mesg:
			print mesg

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
		connectionSocket.settimeout(5)
		mesg = connectionSocket.recv(2048)
		if "get" in mesg:
			print "Get Request"
			print mesg
			print addr
			arg = mesg.split()
			flName = ""
			try:
				flName = arg[1]
				print pathToDirectory + flName
				sendfile = open(pathToDirectory + flName, 'rb')
				data = sendfile.read()
				connectionSocket.send(data) 
				connectionSocket.close() 
				sendfile.close()
			except:
				print "bad request"
		    	break
	    	print "file sent"
		try:
			connectionSocket.close() 
		except:
			print "closing"

		print "Exiting TCP server thread"

def runTCPClient(str,tcp):
	clientSocket = socket(AF_INET,SOCK_STREAM)
	clientSocket.connect(("localhost",tcp))
	clientSocket.send(str)
	modifiedMesg,serverAddress = clientSocket.recvfrom(2048)
	clientSocket.close()
	return modifiedMesg

def openTCPClient(str, adr, tcp, filename):
	clientSocket = socket(AF_INET,SOCK_STREAM)
	clientSocket.connect((adr,tcp))
	clientSocket.send(str)
	LENGTH_SIZE = 4 # length is a 4 byte int.
    # Recieve the file from the client
	writefile = open(pathToDirectory + filename, 'wb')
    #length = decode_length(clientSocket.read(LENGTH_SIZE) # Read a fixed length integer, 2 or 4 bytes
	#while (length):
	rec = clientSocket.recv(102400)
	print rec
	writefile.write(rec)
	#clientSocket.send(b'A') # single character A to prevent issues with buffering
	clientSocket.close()
	writefile.close()
	return "file read"
	
def runUDPClient(str, udp):
	clientSocket = socket(AF_INET,SOCK_DGRAM)	
	clientSocket.sendto(str,("localhost",udp))
	modifiedMesg,serverAddress = clientSocket.recvfrom(2048)
	clientSocket.close()
	return modifiedMesg

def openUDPClient(str, adr, udp):
	clientSocket = socket(AF_INET,SOCK_DGRAM)	
	clientSocket.sendto(str,(adr,udp))
	modifiedMesg = ""
	ready = select.select([clientSocket], [], [], 5)
	if ready[0]:
		modifiedMesg,serverAddress = clientSocket.recvfrom(2048)
	return modifiedMesg

neighbors = []
seqNbr = 0
        
if (len(sys.argv) < 5 or len(sys.argv) == 6 or len(sys.argv) > 7):
    sys.exit("incorrect number of args \n peer.py [PEER NAME] [MY IP] [MY PORT] [PATH TO DIRECTORY] [optional PEER IP] [optional PEER PORT]")
elif (len(sys.argv) == 5):
	print "First peer"
	peername = sys.argv[1]
	myIP = sys.argv[2]
	myPort = sys.argv[3]
	pathToDirectory = sys.argv[4]
	peerIP = ""
	peerPort = ""
elif (len(sys.argv) == 7):
	print "Peer"
	peername = sys.argv[1]
	myIP = sys.argv[2]
	myPort = sys.argv[3]
	pathToDirectory = sys.argv[4]
	peerIP = sys.argv[5]
	peerPort = sys.argv[6]
	neighbors.append("neighbor")
	neighbors.append(str(peerIP))
	neighbors.append(str(peerPort))
else:
    sys.exit("Error message")


files = []
try:
	for (dirpath, dirnames, filenames) in walk(pathToDirectory):
		files.extend(filenames)
		break
except:
		print "Invalid Directory"

print "Peer Name: " + peername
print "My IP: " + myIP
print "My Port: " + myPort
print "Directory: " + pathToDirectory
udpPort = myPort
tcpPort = int(myPort) + 1 
print "TCP Port fileTransferPort: " + str(tcpPort)
print "UDP Port lookupPort: " + udpPort
print peerIP
print peerPort

thread1 = TCPServer(1,int(tcpPort))
thread2 = UDPServer(2,int(udpPort))

thread1.start()
thread2.start()

if (peerIP != ""):
	print openUDPClient("add " + peername + " " +  myIP + " " + myPort, str(peerIP) , int(peerPort))

choice =""
while choice !="quit":
	choice = raw_input('\n' + "Available Commands:, status, find <filename>, get <filename> <target-peer-ip> <target-file-transfer-port>, quit " + '\n\n>')
	if ("status" in choice):
		print "Neighbors: " + str(neighbors)
		files = []
		try:
			for (dirpath, dirnames, filenames) in walk(pathToDirectory):
				files.extend(filenames)
				break
		except:
			print "Invalid Directory"
		print "Files: " + str(files)
	if ("find" in choice):
		try:
			start = choice.index(' ')
			filename = choice[start+1:]
		except:
			print "incorrect argument"
		print "finding: " + filename
		if filename in files:
			print "you already have the file: " + filename
		else:
			for counter in xrange(0,len(neighbors),3):
				print openUDPClient("find " + filename + " " + peername + " " + myIP + " " + str(myPort) + " " + str(seqNbr), neighbors[counter+1], int(neighbors[counter+2]))
			seqNbr += 1
	if ("get" in choice):
		args = choice.split()
		try:
			name = args[1]
			targIP = args[2]
			targPort = args[3]
		except:
			print "incorrect args"
			break
		mesg = openTCPClient("get " + name, targIP, int(targPort), name)
		print mesg


#Send stop message to threads	
thread1.done=True
thread2.done=True

# #if blocking in thread1 and thread2, you can send "pings" from here to both those ports to force them out of blocking and check the loop condition
runTCPClient("quit",int(tcpPort))
runUDPClient("quit",int(udpPort))
print "Waiting for all threads to complete"
thread1.join()
thread2.join()

print "Exiting Main Thread"

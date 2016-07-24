# -*- coding=utf-8 -*-
import os
import sys
import socket
import threading

class sendHandler(threading.Thread):
	
	def __init__(self,sSock,dSock):
		super(sendHandler, self).__init__()
		self.sSock = sSock
		self.dSock = dSock
		
	def run(self):
		while 1:
			data = self.sSock.recv(1024)
			self.dSock.send(data)

class recvHandler(threading.Thread):

	def __init__(self,sSock,dSock):
		super(recvHandler, self).__init__()
		self.sSock = sSock
		self.dSock = dSock
		
	def run(self):
		while 1:
			data = self.dSock.recv(1024)
			self.sSock.send(data)
	

class Delegate:
	
	def __init__(self,**keys):
		if keys.has_key("shost") and keys.has_key("sport") and keys.has_key("dhost") and keys.has_key("dport"):
			self.dhost = keys["dhost"]
			self.dport = keys["dport"]
			self.sSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.sSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			self.sSock.bind((keys["shost"],keys["sport"]))
			self.sSock.listen(10)
		else:
			raise "key error"
	
	def run(self):
		while 1:
			clisock,cliaddr = self.sSock.accept()
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			try:
				sock.connect((self.dhost,self.dport))
			except:
				print "Connect failed"
				continue
			sendHandler(clisock,sock).start()
			recvHandler(clisock,sock).start()
			

from threading import *
from socket import *
from GamePacket import *
import time

class GameClientWorker(Thread):
	def __init__(self, server, client):
		self.lastRequest = time.time()
		self.server = server
		self.connected = False
		self.willDisconnect = False
		self.clientSocket, self.clientAddress = client
		self.clientSocket.settimeout(1.5)
		Thread.__init__(self)
		self.daemon = True
		self.start()

	def sendPacket(self, packet):
		try:
			self.clientSocket.sendall(packet.serializeData())
		except error as e:
			if self.server.handler is not None:
				self.server.handler(e)

	def isConnected(self):
		return self.connected

	def isClientAlive(self):
		# 10 sec timeout
		alive = self.lastRequest+10.0 > time.time()
		if not alive:
			print "Client %s is timeout" % (str(self.clientAddress))
		return alive

	def closeSocket(self):
		self.willDisconnect = True

	def run(self):
		print "Client %s connected" % (str(self.clientAddress))
		self.connected = True
		self.lastRequest = time.time()
		while not self.willDisconnect and self.isClientAlive():
			try:
				data = self.clientSocket.recv(1024)
				if data is None:
					continue
				packet = GamePacket.parsePacket(data)
				if packet is not None:
					self.lastRequest = time.time()
				if self.server.listener is not None:
					self.server.listener(self, packet)
			except Exception:
				continue
		try:
			self.clientSocket.shutdown(SHUT_RDWR)
			self.clientSocket.close()
		except Exception:
			pass
		self.connected = False

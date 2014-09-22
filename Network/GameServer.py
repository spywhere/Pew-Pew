from threading import *
from socket import *
from GamePacket import *
from GameClientWorker import *

class GameServer(Thread):
	clients = []
	def __init__(self, port, listener=None, handler=None):
		self.lock = Lock()
		self.port = port
		self.listener = listener
		self.handler = handler
		self.connected = False
		self.willDisconnect = False
		Thread.__init__(self)
		self.daemon = True
		self.start()

	def serverLock(self):
		self.lock.acquire(True)

	def serverUnlock(self):
		self.lock.release()

	def setListener(self, listener):
		self.listener = listener

	def setHandler(self, handler):
		self.handler = handler

	def run(self):
		try:
			self.serverSocket = socket(AF_INET, SOCK_STREAM)
			self.serverSocket.bind(("", self.port))
			self.serverSocket.listen(1)
			self.serverSocket.settimeout(1.5)
			self.connected = True
		except error as e:
			self.serverSocket = None
			self.connected = False
			if self.handler is not None:
				self.handler(e)
		while self.connected and not self.willDisconnect:
			try:
				self.clients.append(GameClientWorker(self, self.serverSocket.accept()))
			except timeout as t:
				continue
		# self.sendPacket(DisconnectPacket())
		for client in self.clients:
			client.closeSocket()
			import time
			disconnectTimeout = time.time()
			while client.isConnected() and disconnectTimeout+3.0 > time.time():
				continue
		if self.serverSocket is not None:
			try:
				self.serverSocket.shutdown(SHUT_RDWR)
				self.serverSocket.close()
			except Exception:
				pass
		self.connected = False

	def isConnected(self):
		return self.connected

	def sendPacket(self, packet, targetClient=None):
		try:
			for client in self.clients:
				packet.setMe(targetClient is not None and targetClient == client)
				client.sendPacket(packet)
		except error as e:
			if self.handler is not None:
				self.handler(e)

	def closeSocket(self):
		self.willDisconnect = True

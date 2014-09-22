from ParticlePlay import Scene
from Network import *
from GameServerScene import *

class ServerBindScene(Scene):
	port = 5555
	error = None
	progress = 0
	delay = 0

	def onInit(self):
		# self.port = raw_input("Enter server port: ")
		self.bind()
		self.retry = 3.0
		self.error = None

	def bind(self):
		self.socket = GameServer(int(self.port), handler=self.handleError)

	def handleError(self, error):
		self.error = error

	def onRender(self, renderer, delta):
		if self.error is not None:
			renderer.drawString((10, 35), "Connection failed: " + self.error.strerror)
			return
		if self.port is not None:
			renderer.drawString((10, 35), "Starting server"+("."*(self.progress+1)))

	def onUpdate(self, gameInput, delta):
		if self.error is not None:
			self.retry -= delta
			if self.retry <= 0:
				self.connect()
		if self.port is not None:
			if self.delay > 0:
				self.delay -= 1
			else:
				self.delay = 10
				self.progress += 1
				self.progress %= 3
			if self.socket is not None and self.socket.isConnected():
				self.getGame().enterScene(GameServerScene(self.socket))

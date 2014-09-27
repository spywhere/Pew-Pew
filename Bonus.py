from ParticlePlay import Color
import math
import time

class Bonus:
	def __init__(self, position=[0, 0], size=5):
		self.timeout = time.time()
		self.bid = 0
		self.position = position
		self.totalBullet = 7
		self.size = size
		self.alive = True

	def onRender(self, renderer):
		oldColor = renderer.getColor()
		renderer.setColor(Color(128, 255, 128))
		renderer.fillRoundRect(self.position, (self.size, self.size), True)
		renderer.setColor(oldColor)

	def onUpdate(self, delta):
		pass

	def setBonusId(self, bid):
		self.bid = bid

	def getBonusId(self):
		return self.bid

	def resetTimeout(self):
		self.timeout = time.time()

	def isTimeout(self):
		return self.timeout+1.0 < time.time()

	def isAlive(self):
		return self.alive

	def getTotalBullet(self):
		if not self.alive:
			return 0
		return self.totalBullet

	def setPosition(self, position):
		self.position = position

	def getPosition(self):
		return self.position

	def getSize(self):
		return self.size

	def kill(self):
		self.alive = False

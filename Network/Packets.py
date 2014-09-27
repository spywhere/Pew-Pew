from GamePacket import *

class RequestGameStatePacket(GamePacket):
	@classmethod
	def getPacketId(cls):
		return 1

class PlayerInfoPacket(GamePacket):
	def __init__(self, position=[-1, -1], velocity=[0, 0], angle=0, health=0, pid=0):
		self.pid = pid
		self.x = position[0]
		self.y = position[1]
		self.vx = velocity[0]
		self.vy = velocity[1]
		self.angle = angle
		self.health = health

	@classmethod
	def getPacketId(cls):
		return 2

	@classmethod
	def fromString(cls, data):
		datacomponents = data.split(",")
		if len(datacomponents) >= 7:
			try:
				pid = int(datacomponents[0])
				x = float(datacomponents[1])
				y = float(datacomponents[2])
				vx = int(datacomponents[3])
				vy = int(datacomponents[4])
				angle = float(datacomponents[5])
				health = int(datacomponents[6])
				return PlayerInfoPacket([x, y], [vx, vy], angle, health, pid)
			except Exception:
				pass
		return None

	def toString(self):
		return "%d,%f,%f,%d,%d,%f,%d" % (self.pid, self.x, self.y, self.vx, self.vy, self.angle, self.health)

	def getPlayerId(self):
		return self.pid

	def getPosition(self):
		return (self.x, self.y)

	def getVelocity(self):
		return (self.vx, self.vy)

	def getAngle(self):
		return self.angle

	def getHealth(self):
		return self.health

class BulletInfoPacket(GamePacket):
	def __init__(self, position=[-1, -1], velocity=[0, 0], alive=True, bid=0):
		self.bid = bid
		self.x = position[0]
		self.y = position[1]
		self.vx = velocity[0]
		self.vy = velocity[1]
		self.alive = alive

	@classmethod
	def getPacketId(cls):
		return 3

	@classmethod
	def fromString(cls, data):
		datacomponents = data.split(",")
		if len(datacomponents) >= 5:
			try:
				alive = bool(int(datacomponents[0][0]))
				bid = int(datacomponents[0][1:])
				x = float(datacomponents[1])
				y = float(datacomponents[2])
				vx = int(datacomponents[3])
				vy = int(datacomponents[4])
				return BulletInfoPacket([x, y], [vx, vy], alive, bid)
			except Exception:
				pass
		return None

	def toString(self):
		return "%1d%d,%f,%f,%d,%d" % (self.alive, self.bid, self.x, self.y, self.vx, self.vy)

	def getBulletId(self):
		return self.bid

	def getPosition(self):
		return (self.x, self.y)

	def getVelocity(self):
		return (self.vx, self.vy)

	def isAlive(self):
		return self.alive

class BonusInfoPacket(GamePacket):
	def __init__(self, position=[-1, -1], alive=True, bid=0):
		self.bid = bid
		self.x = position[0]
		self.y = position[1]
		self.alive = alive

	@classmethod
	def getPacketId(cls):
		return 4

	@classmethod
	def fromString(cls, data):
		datacomponents = data.split(",")
		if len(datacomponents) >= 3:
			try:
				alive = bool(int(datacomponents[0][0]))
				bid = int(datacomponents[0][1:])
				x = float(datacomponents[1])
				y = float(datacomponents[2])
				return BonusInfoPacket([x, y], alive, bid)
			except Exception:
				pass
		return None

	def toString(self):
		return "%1d%d,%f,%f" % (self.alive, self.bid, self.x, self.y)

	def getBonusId(self):
		return self.bid

	def getPosition(self):
		return (self.x, self.y)

	def isAlive(self):
		return self.alive

class PlayerGunPacket(GamePacket):
	def __init__(self, reloading=False, bulletInMagazine=0, totalBullet=0):
		self.reloading = reloading
		self.bulletInMagazine = bulletInMagazine
		self.totalBullet = totalBullet

	@classmethod
	def getPacketId(cls):
		return 5

	@classmethod
	def fromString(cls, data):
		datacomponents = data.split(",")
		if len(datacomponents) >= 2:
			try:
				reloading = bool(int(datacomponents[0][0]))
				bulletInMagazine = int(datacomponents[0][1:])
				totalBullet = int(datacomponents[1])
				return PlayerGunPacket(reloading, bulletInMagazine, totalBullet)
			except Exception:
				pass
		return None

	def toString(self):
		return "%1d%d,%d" % (self.reloading, self.bulletInMagazine, self.totalBullet)

	def isReloading(self):
		return self.reloading

	def getBulletInMagazine(self):
		return self.bulletInMagazine

	def getTotalBullet(self):
		return self.totalBullet

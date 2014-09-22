from Bullet import *

class Gun:
	reloadingTime = 0
	cooldownTime = 0
	def __init__(self, bulletPerMagazine=0, totalBullet=0, reloadTime=3.0, cooldown=0.2):
		self.bulletInMagazine = bulletPerMagazine
		self.bulletPerMagazine = bulletPerMagazine
		self.totalBullet = totalBullet
		self.reloadTime = reloadTime
		self.cooldown = cooldown
		self.localReload = False

	def setBulletInMagazine(self, bulletInMagazine):
		self.bulletInMagazine = bulletInMagazine

	def getBulletInMagazine(self):
		return self.bulletInMagazine

	def setBulletPerMagazine(self, bulletPerMagazine):
		self.bulletInMagazine = bulletPerMagazine
		self.bulletPerMagazine = bulletPerMagazine

	def getBulletPerMagazine(self):
		return self.bulletPerMagazine

	def setTotalBullet(self, totalBullet):
		self.totalBullet = totalBullet

	def getTotalBullet(self):
		return self.totalBullet

	def setReload(self, reloading):
		self.localReload = reloading

	def isReloading(self):
		return self.reloadingTime > 0 or self.localReload

	def isCooldown(self):
		return self.cooldownTime > 0

	def getBulletPerShot(self):
		return 1

	def getBullet(self, position, angle, minimumDistance):
		# speed = 500
		# position = [px+math.sin(angle)*minimumDistance, py+math.cos(angle)*minimumDistance]
		# velocity = [math.sin(angle)*speed, math.cos(angle)*speed]
		return Bullet(position, angle, minimumDistance)

	def shoot(self, player, angle, minimumDistance=10):
		if self.reloadingTime > 0 or self.cooldownTime > 0:
			return []
		if self.bulletInMagazine <= 0:
			if self.totalBullet > 0:
				self.reload()
			return []
		self.bulletInMagazine -= 1
		self.cooldownTime = self.cooldown
		bullets = []
		for i in range(self.getBulletPerShot()):
			bullets.append(self.getBullet(player.getPosition(), angle, minimumDistance))
		return bullets

	def onRender(self, renderer):
		pass

	def reload(self):
		if self.reloadingTime <= 0:
			self.reloadingTime = self.reloadTime

	def onUpdate(self, delta):
		if self.cooldownTime > 0:
			self.cooldownTime -= delta
		if self.reloadingTime > 0:
			self.reloadingTime -= delta
			if self.reloadingTime <= 0:
				self.reloadingTime = 0
				if self.totalBullet > 0:
					bulletLeft = self.bulletInMagazine
					if self.totalBullet+bulletLeft < self.bulletPerMagazine:
						self.bulletInMagazine = self.totalBullet+bulletLeft
						self.totalBullet = 0
					else:
						self.bulletInMagazine = self.bulletPerMagazine
						self.totalBullet -= self.bulletPerMagazine - bulletLeft

from ParticlePlay import Color
from Gun import *
import random
import math
import time

class Player:
	def __init__(self, game, position=[0, 0], color=Color(255, 127, 127), bot=False):
		self.timeout = time.time()
		self.pid = 0
		self.game = game
		self.speed = 200
		self.health = 100
		self.angle = 0
		self.position = position
		self.color = color
		self.gun = Gun(7, 21)
		self.velocity = [0, 0]
		self.bot = bot

	def shoot(self):
		return self.gun.shoot(self, self.angle, 10)

	def onRender(self, renderer):
		oldColor = renderer.getColor()
		renderer.setColor(self.color)
		renderer.drawOval(self.position, [20, 20])

		renderer.setColor(Color(192, 192, 192))
		px, py = self.position
		renderer.drawPolygon([(px+math.sin(self.angle)*8, py+math.cos(self.angle)*8), (px+math.sin(self.angle-(math.pi/4))*5, py+math.cos(self.angle-(math.pi/4))*5), (px+math.sin(self.angle+(math.pi/4))*5, py+math.cos(self.angle+(math.pi/4))*5)])

		renderer.setColor(Color(127, 127, 127))
		renderer.drawRect([px-12, py-17], [25, 2])
		if self.health > 0:
			renderer.setColor(Color(127, 255, 127))
			renderer.fillRect([px-12, py-17], [self.health*25/100, 2])

		renderer.setColor(oldColor)

	def doAI(self):
		angle_deg = self.angle*180/math.pi
		angle_deg += (random.randint(0, 44)-22)
		self.angle = angle_deg*math.pi/180
		x, y = self.position
		w, h = self.game.getSize()
		# min(x*5/100, 5)
		# min((w-x)*5/(w-100), 5)
		# min(y*5/100, 5)
		# min((h-y)*5/(h-100), 5)
		friction_offset = 20
		max_speed = 200 # 3
		self.setSpeed(min(min((x-friction_offset)*max_speed/friction_offset, max_speed), min((w-x-friction_offset)*max_speed/friction_offset, max_speed), min((y-friction_offset)*max_speed/friction_offset, max_speed), min((h-y-friction_offset)*max_speed/friction_offset, max_speed)))
		vx, vy = self.velocity
		vx = math.sin(self.angle)*self.getSpeed()
		vy = math.cos(self.angle)*self.getSpeed()
		self.velocity = [vx, vy]

	def onUpdate(self, delta):
		if self.isBot():
			self.doAI()

		x, y = self.position
		vx, vy = self.velocity
		x += vx*delta
		y += vy*delta
		self.position = [x, y]
		self.gun.onUpdate(delta)

	def isBot(self):
		return self.bot

	def setPlayerId(self, pid):
		self.pid = pid

	def getPlayerId(self):
		return self.pid

	def setPosition(self, position):
		self.position = position

	def getPosition(self):
		return self.position

	def setVelocity(self, velocity):
		self.velocity = velocity

	def getVelocity(self):
		return self.velocity

	def setSpeed(self, speed):
		self.speed = speed

	def getSpeed(self):
		return self.speed

	def setGun(self, gun):
		self.gun = gun

	def getGun(self):
		return self.gun

	def setAngle(self, angle):
		self.angle = angle

	def getAngle(self):
		return self.angle

	def setHealth(self, health):
		self.health = health

	def getHealth(self):
		return self.health

	def resetTimeout(self):
		self.timeout = time.time()

	def isDead(self):
		return self.health <= 0 or self.timeout+10.0 < time.time()

	def isIntersectBullet(self, bullet):
		px, py = self.position
		bx, by = bullet.getPosition()
		distance = math.sqrt(((px-bx)**2)+((py-by)**2))
		return distance < 10+(bullet.getSize()/2)

	def takeDamage(self, bullet):
		if self.isBot():
			self.setSpeed(1)
		self.health -= bullet.getDamage()
		if self.health < 0:
			self.health = 0
		bullet.kill()

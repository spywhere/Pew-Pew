from ParticlePlay import Color
from Gun import *
import random
import math
import time


class Player:
    def __init__(self, game, position=[0, 0], color=Color(255, 127, 127),
                 bot=False):
        self.name = "Unknown"
        self.pid = 0
        self.game = game
        self.color = color
        self.bot = bot
        self.speed = 200
        self.delegate = None
        self.death = 0
        self.respawn(position)
        self.death = 0

    def respawn(self, position):
        self.death += 1
        self.respawnTime = 3
        self.timeout = time.time()
        self.health = 100
        self.velocity = [0, 0]
        self.gun = Gun(7, 21)
        self.position = position
        self.angle = 0
        return self

    def shoot(self):
        if self.respawnTime > 0:
            return []
        return self.gun.shoot(self, self.angle, 10)

    def onRender(self, renderer):
        oldColor = renderer.getColor()
        renderer.setColor(self.color)
        if self.respawnTime > 0:
            renderer.setColor(Color(100, 100, 100))
        renderer.drawOval(self.position, [20, 20])

        renderer.setColor(Color(192, 192, 192))
        px, py = self.position
        renderer.drawPolygon([
            (px+math.sin(self.angle)*8, py+math.cos(self.angle)*8),
            (
                px+math.sin(self.angle-(math.pi/4))*5,
                py+math.cos(self.angle-(math.pi/4))*5
            ), (
                px+math.sin(self.angle+(math.pi/4))*5,
                py+math.cos(self.angle+(math.pi/4))*5
            )
        ])

        if ((not self.delegate and self.respawnTime <= 0) or
                (self.delegate and self.delegate(self, "HealthBar"))):
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
        max_speed = 200  # 3
        self.setSpeed(
            min(
                min((x-friction_offset)*max_speed/friction_offset, max_speed),
                min((w-x-friction_offset)*max_speed/friction_offset, max_speed),
                min((y-friction_offset)*max_speed/friction_offset, max_speed),
                min((h-y-friction_offset)*max_speed/friction_offset, max_speed)
            )
        )
        vx, vy = self.velocity
        vx = math.sin(self.angle)*self.getSpeed()
        vy = math.cos(self.angle)*self.getSpeed()
        self.velocity = [vx, vy]

    def clamp(self, value, minVal, maxVal):
        return max(minVal, min(value, maxVal))

    def onUpdate(self, delta):
        if self.isBot():
            self.doAI()

        x, y = self.position
        vx, vy = self.velocity
        x += vx*delta
        y += vy*delta
        if self.respawnTime > 0:
            self.respawnTime -= delta
        elif self.respawnTime < 0:
            self.respawnTime = 0
        w, h = self.game.getSize()
        self.position = [
            self.clamp(x, 17, w - 12),
            self.clamp(y, 20, h - 12)
        ]
        self.gun.onUpdate(delta)

    def isBot(self):
        return self.bot

    def setDelegate(self, delegate):
        self.delegate = delegate

    def setPlayerId(self, pid):
        self.pid = pid

    def getPlayerId(self):
        return self.pid

    def setPlayerName(self, name):
        self.name = name

    def getPlayerName(self):
        return self.name

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

    def setDeath(self, death):
        self.death = death

    def getDeath(self):
        return self.death

    def setRespawnTime(self, respawnTime):
        self.respawnTime = respawnTime

    def getRespawnTime(self):
        return max(0, self.respawnTime)

    def resetTimeout(self):
        self.timeout = time.time()

    def isDead(self):
        return self.health <= 0 or self.timeout+3.0 < time.time()

    def isIntersectObject(self, obj):
        px, py = self.position
        bx, by = obj.getPosition()
        distance = math.sqrt(((px-bx)**2)+((py-by)**2))
        return distance < 10+(obj.getSize()/2)

    def takeBonus(self, bonus):
        self.getGun().setTotalBullet(
            self.getGun().getTotalBullet()+bonus.getTotalBullet()
        )
        bonus.kill()

    def takeDamage(self, bullet):
        if self.isBot():
            self.setSpeed(1)
        self.health -= bullet.getDamage()
        if self.health < 0:
            self.health = 0
        bullet.kill()

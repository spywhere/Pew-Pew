import math
import time


class Bullet:
    def __init__(self, position=[0, 0], angle=0, minimumDistance=10, size=5):
        self.timeout = time.time()
        self.bid = 0
        self.speed = 500
        self.angle = angle
        self.position = [
            position[0]+math.sin(angle)*minimumDistance,
            position[1]+math.cos(angle)*minimumDistance
        ]
        self.velocity = [
            math.sin(self.angle)*self.speed, math.cos(self.angle)*self.speed
        ]
        self.damage = 45
        self.size = size
        self.alive = True

    def onRender(self, renderer):
        renderer.drawOval(self.position, (self.size, self.size))

    def onUpdate(self, delta):
        if not self.alive:
            return
        x, y = self.position
        vx, vy = self.velocity
        x += vx*delta
        y += vy*delta
        self.position = [x, y]

    def setBulletId(self, bid):
        self.bid = bid

    def getBulletId(self):
        return self.bid

    def resetTimeout(self):
        self.timeout = time.time()

    def isTimeout(self):
        return self.timeout+1.0 < time.time()

    def isAlive(self):
        return self.alive

    def getDamage(self):
        if not self.alive:
            return 0
        return self.damage

    def setPosition(self, position):
        self.position = position

    def getPosition(self):
        return self.position

    def setVelocity(self, velocity):
        self.velocity = velocity

    def getVelocity(self):
        return self.velocity

    def getSize(self):
        return self.size

    def kill(self):
        self.alive = False

from GamePacket import *


class RequestGameStatePacket(GamePacket):
    @classmethod
    def getPacketId(cls):
        return 1


class PlayerInfoPacket(GamePacket):
    def __init__(self, name="", position=[-1, -1], velocity=[0, 0], angle=0, health=0,
                 death=0, respawnTime=0, pid=0):
        self.pid = pid
        self.name = name
        self.x = position[0]
        self.y = position[1]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.angle = angle
        self.health = health
        self.respawnTime = respawnTime
        self.death = death

    @classmethod
    def getPacketId(cls):
        return 2

    @classmethod
    def fromString(cls, data):
        datacomponents = data.split(",")
        if len(datacomponents) >= 7:
            try:
                pid = int(datacomponents[0])
                name = datacomponents[1]
                x = float(datacomponents[2])
                y = float(datacomponents[3])
                vx = int(datacomponents[4])
                vy = int(datacomponents[5])
                angle = float(datacomponents[6])
                health = int(datacomponents[7])
                respawnTime = float(datacomponents[8])
                death = int(datacomponents[9])
                return PlayerInfoPacket(
                    name,
                    [x, y], [vx, vy], angle, health, death, respawnTime, pid
                )
            except Exception:
                pass
        return None

    def toString(self):
        return "%d,%s,%f,%f,%d,%d,%f,%d,%f,%d" % (
            self.pid, self.name, self.x, self.y, self.vx, self.vy,
            self.angle, self.health, self.respawnTime, self.death
        )

    def getPlayerId(self):
        return self.pid

    def getPlayerName(self):
        return self.name

    def getPosition(self):
        return (self.x, self.y)

    def getVelocity(self):
        return (self.vx, self.vy)

    def getAngle(self):
        return self.angle

    def getHealth(self):
        return self.health

    def getDeath(self):
        return self.death

    def getRespawnTime(self):
        return self.respawnTime


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
        return "%1d%d,%f,%f,%d,%d" % (
            self.alive, self.bid, self.x, self.y, self.vx, self.vy
        )

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
        return "%1d%d,%d" % (
            self.reloading, self.bulletInMagazine, self.totalBullet
        )

    def isReloading(self):
        return self.reloading

    def getBulletInMagazine(self):
        return self.bulletInMagazine

    def getTotalBullet(self):
        return self.totalBullet

from ParticlePlay import Scene
from ParticlePlay import Color
from Network import *
from Bonus import *
from Bullet import *
from Player import *
import time
import random


class GameServerScene(Scene):
    bullets = []
    bonuses = []
    players = {}
    bots = {}
    bid = 1
    bnid = 1
    pid = 1
    pps = 0
    packetCount = 0
    lastTime = time.time()+1.0
    lastBonus = time.time()+10.0

    def __init__(self, serverSocket):
        self.serverSocket = serverSocket
        self.serverSocket.setListener(self.listener)

    def listener(self, client, packet):
        self.serverSocket.serverLock()
        if isinstance(packet, Packets.PlayerInfoPacket):
            if packet.getHealth() > 0:
                if client not in self.players:
                    player = Player(
                        self.getGame(),
                        color=Color(
                            random.randint(127, 255),
                            random.randint(127, 255),
                            random.randint(127, 255)
                        )
                    )
                    player.setPlayerId(self.pid)
                    player.setPlayerName(packet.getPlayerName())
                    self.pid += 1
                    self.players[client] = player
                else:
                    player = self.players[client]
                player.setPosition(packet.getPosition())
                player.setAngle(packet.getAngle())
            self.packetCount += 1
        elif isinstance(packet, Packets.PlayerGunPacket):
            player = self.players[client]
            bullets = player.shoot()
            for bullet in bullets:
                bullet.setBulletId(self.bid)
                self.bid += 1
            self.bullets += bullets
            self.packetCount += 1
        elif packet is not None:
            self.packetCount += 1
            print("Packet received (type " + str(packet) + ")")
        self.serverSocket.serverUnlock()

    def onInit(self):
        self.serverSocket.sendPacket(RequestGameStatePacket())

    def onRender(self, renderer, delta):
        renderer.drawString(
            (10, 20), "Connected Clients: " + str(len(self.players))
        )
        renderer.drawString(
            (10, 35), "Bullets on screen: " + str(len(self.bullets))
        )
        renderer.drawString(
            (10, 50), "Bonuses on screen: " + str(len(self.bonuses))
        )
        renderer.drawString((10, 65), "Packet per second: " + str(self.pps))

        offset = 0
        for player in self.players.values():
            message = "%s: " % (player.getPlayerName())
            if player.getRespawnTime() > 0:
                message = "[respawn in %.2fs] %s" % (
                    player.getRespawnTime(),
                    message
                )
            message += "%s Deaths" % (player.getDeath())
            import Tkinter as tk
            renderer.drawString(
                (self.getGame().getWidth() - 10, 5 + offset),
                message, anchor=tk.NE
            )
            offset += 12

        self.serverSocket.serverLock()
        for bullet in self.bullets:
            bullet.onRender(renderer)
        for bonus in self.bonuses:
            bonus.onRender(renderer)
        for client in self.players:
            player = self.players[client]
            player.onRender(renderer)
        self.serverSocket.serverUnlock()

    def onUpdate(self, gameInput, delta):
        if self.lastTime < time.time():
            self.pps = self.packetCount
            self.packetCount = 0
            self.lastTime = time.time()+1.0

        self.serverSocket.serverLock()

        if len(self.players) == 0:
            self.pid = 1
        if len(self.bullets) == 0:
            self.bid = 1
        if len(self.bonuses) == 0:
            self.bnid = 1

        new_bullets = []
        for bullet in self.bullets:
            bullet.onUpdate(delta)
            w, h = self.getGame().getSize()
            x, y = bullet.getPosition()
            if (x < -(bullet.getSize()/2) or x > w+(bullet.getSize()/2) or
                    y < -(bullet.getSize()/2) or y > h+(bullet.getSize()/2)):
                bullet.kill()

            for player in self.players.values():
                if (player.isIntersectObject(bullet) and
                        player.getRespawnTime() <= 0):
                    player.takeDamage(bullet)

            self.serverSocket.sendPacket(BulletInfoPacket(
                bullet.getPosition(), bullet.getVelocity(),
                bullet.isAlive(), bullet.getBulletId()
            ))
            if bullet.isAlive():
                new_bullets.append(bullet)
        self.bullets = new_bullets

        if self.lastBonus < time.time():
            if len(self.bonuses) < 5:
                w, h = self.getGame().getSize()
                bonus = Bonus([
                    random.randint(10, w-10), random.randint(10, h-10)
                ])
                bonus.setBonusId(self.bnid)
                self.bnid += 1
                self.bonuses.append(bonus)
            self.lastBonus = time.time()+5.0

        new_bonuses = []
        for bonus in self.bonuses:
            bonus.onUpdate(delta)

            for player in self.players.values():
                if player.isIntersectObject(bonus):
                    player.takeBonus(bonus)

            self.serverSocket.sendPacket(BonusInfoPacket(
                bonus.getPosition(), bonus.isAlive(), bonus.getBonusId()
            ))
            if bonus.isAlive():
                new_bonuses.append(bonus)
        self.bonuses = new_bonuses

        new_players = {}
        for client in self.players:
            if client.isClientAlive():
                player = self.players[client]
                ppos = player.getPosition()
                pangle = player.getAngle()
                player.onUpdate(delta)
                if ppos != player.getPosition() or pangle != player.getAngle():
                    position = player.getPosition()
                    if player.getRespawnTime() > 0:
                        position = [-1, -1]

                    self.serverSocket.sendPacket(
                        PlayerInfoPacket(
                            player.getPlayerName(),
                            position, player.getVelocity(),
                            player.getAngle(), player.getHealth(),
                            player.getDeath(), player.getRespawnTime(),
                            player.getPlayerId()
                        ), client
                    )
                client.sendPacket(
                    PlayerGunPacket(
                        player.getGun().isReloading(),
                        player.getGun().getBulletInMagazine(),
                        player.getGun().getTotalBullet())
                )
                if not player.isDead():
                    player.resetTimeout()
                    new_players[client] = player
                else:
                    w, h = self.getGame().getSize()
                    new_players[client] = player.respawn([w/2, h/2])

        self.players = new_players

        self.serverSocket.serverUnlock()
        if gameInput.isKeyDown("escape"):
            self.getGame().stopGame()

    def onExit(self):
        self.serverSocket.closeSocket()
        disconnectTimeout = time.time()
        while (self.serverSocket.isConnected() and
                disconnectTimeout+3.0 > time.time()):
            continue

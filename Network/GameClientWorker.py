from socket import *
from GamePacket import *
import time


class GameClientWorker():
    def __init__(self, server, clientAddress):
        self.server = server
        self.connected = True
        self.lastRequest = time.time()
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientAddress = clientAddress
        self.clientSocket.settimeout(1.5)
        print("Client %s connected" % (str(self.clientAddress)))

    def sendPacket(self, packet):
        try:
            self.clientSocket.sendto(packet.serializeData(), self.clientAddress)
        except error as e:
            if self.server.handler is not None:
                self.server.handler(e)

    def processPacket(self, data):
        try:
            if data is None:
                return
            packet = GamePacket.parsePacket(data)
            if packet is not None:
                self.lastRequest = time.time()
            if self.server.listener is not None:
                self.server.listener(self, packet)
        except:
            return

    def isConnected(self):
        return self.connected

    def isClientAlive(self):
        # 3 sec timeout
        alive = self.lastRequest+3.0 > time.time()
        if not alive:
            print("Client %s is timeout" % (str(self.clientAddress)))
        return alive

    def closeSocket(self):
        try:
            self.clientSocket.shutdown(SHUT_RDWR)
            self.clientSocket.close()
        except Exception:
            pass
        self.connected = False

from threading import *
from socket import *
from GamePacket import *
import time


class GameSocket(Thread):
    def __init__(self, host, port, listener=None, handler=None):
        self.lock = Lock()
        self.lastRequest = time.time()
        self.host = host
        self.port = port
        self.listener = listener
        self.handler = handler
        self.connected = False
        self.willDisconnect = False
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def clientLock(self):
        self.lock.acquire(True)

    def clientUnlock(self):
        self.lock.release()

    def setListener(self, listener):
        self.listener = listener

    def setHandler(self, handler):
        self.handler = handler

    def isServerAlive(self):
        # 3 sec timeout
        alive = self.lastRequest+3.0 > time.time()
        if not alive:
            print("Server is timeout")
        return alive

    def run(self):
        try:
            self.lastRequest = time.time()
            self.clientSocket = socket(AF_INET, SOCK_DGRAM)
            # self.clientSocket.connect((self.host, self.port))
            self.connected = True
        except error as e:
            self.clientSocket = None
            self.connected = False
            if self.handler is not None:
                self.handler(e)
        while (self.connected and not self.willDisconnect and
                self.isServerAlive()):
            try:
                data, serverAddress = self.clientSocket.recvfrom(1024)
                if data is None:
                    continue
                packet = GamePacket.parsePacket(data)
                if packet is not None:
                    self.lastRequest = time.time()
                if self.listener is not None:
                    self.listener(packet)
            except error as e:
                print("Server Error: ", e)
                break
        if self.clientSocket is not None:
            try:
                self.clientSocket.shutdown(SHUT_RDWR)
                self.clientSocket.close()
            except Exception:
                pass
        self.connected = False

    def isConnected(self):
        return self.connected

    def sendPacket(self, packet):
        try:
            self.clientSocket.sendto(
                packet.serializeData(), (self.host, self.port)
            )
            # self.clientSocket.sendall(packet.serializeData())
        except error as e:
            if self.handler is not None:
                self.handler(e)

    def closeSocket(self):
        self.willDisconnect = True

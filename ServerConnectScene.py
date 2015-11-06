from ParticlePlay import Scene
from Network import *
from GameScene import *


class ServerConnectScene(Scene):
    error = None
    progress = 0
    delay = 0

    def __init__(self, host, port=5555, msg=""):
        self.host = host
        self.port = port
        self.msg = msg
        if msg != "":
            self.connect()

    def connect(self):
        self.retry = 3.0
        self.socket = GameSocket(self.host, self.port, handler=self.handleError)
        self.error = None

    def onInit(self):
        self.connect()

    def handleError(self, error):
        self.error = error

    def onRender(self, renderer, delta):
        if self.msg is not None and self.msg != "":
            renderer.drawString((10, 35), self.msg)
        if self.error is not None:
            renderer.drawString(
                (10, 50), "Connection failed: " + self.error.strerror
            )
            return
        if self.host is not None:
            renderer.drawString(
                (10, 50), "Connecting to server"+("."*(self.progress+1))
            )

    def onUpdate(self, gameInput, delta):
        if self.error is not None:
            self.retry -= delta
            if self.retry <= 0:
                self.connect()
        if self.host is not None:
            if self.delay > 0:
                self.delay -= 1
            else:
                self.delay = 10
                self.progress += 1
                self.progress %= 3
            if self.socket is not None and self.socket.isConnected():
                print "Connected"
                self.socket.sendPacket(RequestGameStatePacket())
                self.getGame().enterScene(GameScene(self.socket))

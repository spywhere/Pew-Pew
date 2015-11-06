from ParticlePlay import *
from ServerBindScene import *


class PewPewServer(Game):
    def __init__(self):
        self.setDebugMode(True)
        self.setTitle("Pew Pew! [Server]")
        self.setSize((800, 600))
        self.setTargetFPS(60)
        self.setVSync(True)
        self.enterScene(ServerBindScene())

PewPewServer()

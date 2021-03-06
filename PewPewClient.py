from ParticlePlay import *
# from GameScene import *
from ServerConnectScene import *


class PewPewClient(Game):
    def __init__(self):
        self.setDebugMode(True)
        self.setTitle("Pew Pew!")
        self.setSize((800, 600))
        self.setTargetFPS(60)
        self.setVSync(True)
        host = raw_input("Enter server host: ")
        username = raw_input("Enter username: ")
        self.enterScene(ServerConnectScene(username, host))

PewPewClient()

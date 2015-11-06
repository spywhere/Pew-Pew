from Game import *
from abc import abstractmethod


class Scene:
    game = None
    name = None

    def enterScene(self, gameScene):
        self.game.enterScene(gameScene)

    def getGame(self):
        return self.game

    @abstractmethod
    def onInit(self):
        print "Scene " + self.name + " initialized."

    @abstractmethod
    def onRender(self, renderer, delta):
        print "Scene " + self.name + " rendered."

    @abstractmethod
    def onUpdate(self, input, delta):
        print "Scene " + self.name + " updated."

    def willExit(self):
        return True

    def onExit(self):
        pass

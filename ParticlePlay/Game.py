from Input import *
from Renderer import *
from Scene import *
from Color import *
import Tkinter as tk
import time


class Game:
    _debugMode = False
    _PSInfo = [-1, -1, -1]
    _infoText = "-1 FPS -1 UPS [0.00ms]"
    _mainWindow = None
    _mainCanvas = None
    _renderer = None
    _gameInput = None
    _currentScene = None
    _title = "ParticlePlay Game"
    _gameBG = Color(0, 0, 0)
    _size = (640, 480)
    _targetFPS = 30
    _targetUPS = 30
    _vSync = False
    _showFPS = True
    _running = False
    _idleTime = 0.002
    _gameScenes = {}

    def setDebugMode(self, debug):
        self._debugMode = debug

    def setTitle(self, title):
        self._title = title
        if self._mainWindow is not None:
            self._mainWindow.title(title)

    def setSize(self, size):
        self._size = size

    def getSize(self):
        return self._size

    def getWidth(self):
        return self._size[0]

    def getHeight(self):
        return self._size[1]

    def setGameBG(self, color):
        self._gameBG = color

    def setTargetFPS(self, targetFPS):
        self._targetFPS = targetFPS

    def setTargetUPS(self, targetUPS):
        self._targetUPS = targetUPS

    def setIdleTime(self, idleTime):
        self._idleTime = idleTime

    def setShowFPS(self, showFPS):
        self._showFPS = showFPS

    def setVSync(self, vSync):
        self._vSync = vSync

    def getFPS(self):
        return self._PSInfo[0]

    def getUPS(self):
        return self._PSInfo[1]

    def addScene(self, sceneName, gameScene):
        gameScene.game = self
        gameScene.name = sceneName
        self._gameScenes[sceneName] = gameScene

    def getScene(self, sceneName):
        return self._gameScenes[sceneName]

    def removeScene(self, sceneName):
        del self._gameScenes[sceneName]

    def enterScene(self, scene, sceneName="UntitledScene"):
        if isinstance(scene, str):
            scene = self.getScene(scene)
        elif isinstance(scene, Scene):
            self.addScene(sceneName, scene)
        if scene is not None:
            if self._debugMode:
                if sceneName == "UntitledScene":
                    print "Enter a new scene"
                else:
                    print "Current Scene: " + scene.name
            startGame = self._currentScene is None
            self._currentScene = scene.name
            scene.onInit()
            if startGame:
                self.startGame()

    def startGame(self):
        if self._debugMode:
                print "Initializing game..."
        self._running = True
        self._mainWindow = tk.Tk()
        self._mainWindow.protocol("WM_DELETE_WINDOW", self.stopGame)
        self._mainWindow.title(self._title)
        self._mainWindow.resizable(0, 0)
        self._renderer = Renderer(self)
        self._gameInput = Input(self)
        try:
            self._mainCanvas = tk.Canvas(
                self._mainWindow, width=self._size[0], height=self._size[1],
                borderwidth=0
            )
            self._mainCanvas.pack()
            self._mainCanvas.update()
        except:
            self._mainWindow = None
            if self._debugMode:
                print "!!! Unexpected error occurred on startGame."
            raise
        if self._debugMode:
                print "Game running..."
        lastTimer = self.getTimeMicros()
        lastTime = lastTimer
        renderDelta = 0
        updateDelta = 0
        frames = 0
        updates = 0
        microPerRender = 1000000 / self._targetFPS
        microPerUpdate = 1000000 / self._targetUPS
        while self._running:
            timeNow = self.getTimeMicros()
            timeDelta = (timeNow-lastTime)
            renderDelta += timeDelta
            updateDelta += timeDelta
            lastTime = timeNow

            if updateDelta > microPerUpdate:
                updateDelta -= microPerUpdate
                updates += 1
                if self._currentScene is not None:
                    self._gameScenes[self._currentScene].onUpdate(
                        self._gameInput, timeDelta/1000000.0
                    )
                self._gameInput._update()

            if not self._vSync or renderDelta > microPerRender:
                renderDelta -= microPerRender
                frames += 1
                if self._currentScene is not None:
                    self._renderer.clearAll(self._gameBG)
                    self._gameScenes[self._currentScene].onRender(
                        self._renderer, renderDelta
                    )
                    if self._showFPS:
                        self._renderer.setColor(Color(255, 255, 255))
                        self._renderer.drawString(
                            (10, 5), self._infoText, tk.NW, tk.LEFT
                        )

            self.sleep(self._idleTime)

            if self.getTimeMicros() - lastTimer >= 1000000:
                self._PSInfo = [frames, updates, timeDelta/1000.0]
                self._infoText = "%d FPS, %d UPS [%0.2fms]" % (
                    frames, updates, timeDelta/1000.0
                )
                if self._debugMode:
                    print self._infoText
                frames = 0
                updates = 0
                lastTimer = self.getTimeMicros()
        if self._currentScene is not None:
            self._gameScenes[self._currentScene].onExit()
        tk.sys.exit(0)

    def stopGame(self):
        print "Attempting to close game..."
        if (self._currentScene is not None
                and not self._gameScenes[self._currentScene].willExit()):
            return
        if self._debugMode:
                print "Closing game..."
        self._running = False

    def getTimeMicros(self):
        return int(round(time.time() * 1000000))

    def sleep(self, secs):
        if self._mainWindow is None:
            time.sleep(secs)
        else:
            self._mainWindow.update_idletasks()
            self._mainWindow.after(int(1000 * secs), self._mainWindow.quit)
            self._mainWindow.mainloop()

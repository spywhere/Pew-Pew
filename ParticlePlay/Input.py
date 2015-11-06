class Input:
    _game = None
    _keydown = {}
    _keywaiting = {}
    # This holds an unprocessed key release.  We delay key releases by up to
    # one call to keys_pressed() to get round a problem with auto repeat.
    _cooldown = 0
    _keyrelease = None
    _mousedown = [False, False, False]
    _mouseposition = [(-1, -1), (-1, -1), (-1, -1)]

    def __init__(self, game):
        self._game = game
        self._game._mainWindow.bind("<KeyPress>", self._keypress)
        self._game._mainWindow.bind("<KeyRelease>", self._keyrelease)
        self._game._mainWindow.bind("<FocusIn>", self._clear_keys)
        self._game._mainWindow.bind("<FocusOut>", self._clear_keys)
        self._game._mainWindow.bind("<Button-1>", self._leftclick)
        self._game._mainWindow.bind("<Button-2>", self._rightclick)
        self._game._mainWindow.bind("<Button-3>", self._middleclick)

        self._game._mainWindow.bind("<B1-Motion>", self._leftdown)
        self._game._mainWindow.bind("<B2-Motion>", self._rightdown)
        self._game._mainWindow.bind("<B3-Motion>", self._middledown)

        self._game._mainWindow.bind("<Motion>", self._mousemove)

    def isKeyDown(self, key):
        return (
            self._keydown is not None and str.lower(key) in self._keydown
            and self._keydown[str.lower(key)]
        )

    def isKeyUp(self, key):
        return not self.isKeyDown(key)

    def isMouseDown(self, button=0, cooldown=0):
        if self._isCoolDown():
            return False
        mousedown = (
            self._mousedown[button] is not None and self._mousedown[button]
        )
        if mousedown:
            self._cooldown = cooldown
        return mousedown

    def _isCoolDown(self):
        return self._cooldown > 0

    def getMousePosition(self, button=0):
        return self._mouseposition[button]

    def _leftdown(self, event):
        self._mousedown[0] = True
        self._mouseposition[0] = (event.x, event.y)

    def _rightdown(self, event):
        self._mousedown[1] = True
        self._mouseposition[1] = (event.x, event.y)

    def _middledown(self, event):
        self._mousedown[2] = True
        self._mouseposition[2] = (event.x, event.y)

    def _keypress(self, event):
        self._keydown[str.lower(event.keysym)] = True
        self._keywaiting[str.lower(event.keysym)] = True
        # print event.char, event.keycode
        self._keyrelease = True

    def _keyrelease(self, event):
        try:
            del self._keydown[str.lower(event.keysym)]
        except:
            pass
        self._keyrelease = True

    def _mousemove(self, event):
        self._mouseposition[0] = (event.x, event.y)
        self._mouseposition[1] = (event.x, event.y)
        self._mouseposition[2] = (event.x, event.y)

    def _leftclick(self, event):
        self._mousedown[0] = True
        self._mouseposition[0] = (event.x, event.y)

    def _rightclick(self, event):
        self._mousedown[1] = True
        self._mouseposition[1] = (event.x, event.y)

    def _middleclick(self, event):
        self._mousedown[2] = True
        self._mouseposition[2] = (event.x, event.y)

    def _clearmouse(self):
        self._mousedown = [False, False, False]

    def _clear_keys(self, event=None):
        self._keydown = {}
        self._keywaiting = {}
        self._keyrelease = False

    def _update(self):
        self._clearmouse()
        if self._cooldown > 0:
            self._cooldown -= 1

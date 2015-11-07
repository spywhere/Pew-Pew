from Renderer3D import *
from Color import *
import Tkinter as tk


class Renderer:
    _render3d = None
    _game = None
    _fgColor = Color(255, 255, 255)
    _bgColor = Color(0, 0, 0)
    _strokeSize = 1

    def __init__(self, game):
        self._game = game
        self._render3d = Renderer3D(self)
        self.setPostOffset(
            [self._game.getWidth() / 2, self._game.getHeight() / 2]
        )

    def _isOutside(self, coords):
        for coord in coords:
            if (coord[0] >= 0 and coord[1] >= 0 and
                coord[0] < self._game.getWidth() and
                    coord[1] < self._game.getHeight()):
                return False
        return True

    def _toCoord(self, coords):
        c = []
        for coord in coords:
            p = self._getPosition(coord)
            c.append(p[0])
            c.append(p[1])
        return c

    def _getPosition(self, positions):
        if ((isinstance(positions, list) or isinstance(positions, tuple)) and
                (
                    isinstance(positions[0], int) or
                    isinstance(positions[0], float)
                )):
            return self._render3d._getPosition(positions)
        npos = []
        for pos in positions:
            npos.append(self._getPosition(pos))
        return npos

    def _toOvalCoord(self, position, size):
        if len(position) == 2 and len(size) == 2:
            return [
                (position[0]-size[0]/2, position[1]-size[1]/2),
                (position[0]-size[0]/2, position[1]+size[1]/2),
                (position[0]+size[0]/2, position[1]+size[1]/2),
                (position[0]-size[0]/2, position[1]+size[1]/2)
            ]
        else:
            print("Position and size must be at least 2-tuple")
            raise Exception

    def _toRectCoord(self, position, size):
        c = []
        if len(position) == 3 and len(size) >= 2:
            # Rectangle on 3D
            c.append((position[0], position[1], position[2]))
            c.append((position[0]+size[0], position[1], position[2]))
            c.append((position[0]+size[0], position[1]+size[1], position[2]))
            c.append((position[0], position[1]+size[1], position[2]))
            if len(size) == 3:
                # Cube
                c.append((position[0], position[1], position[2]+size[2]))
                c.append(
                    (position[0]+size[0], position[1], position[2]+size[2])
                )
                c.append((
                    position[0]+size[0], position[1]+size[1],
                    position[2]+size[2]
                ))
                c.append(
                    (position[0], position[1]+size[1], position[2]+size[2])
                )
            return c
        elif len(position) == 2 and len(size) == 2:
            # Rectangle
            return [
                (position[0], position[1]),
                (position[0]+size[0], position[1]),
                (position[0]+size[0], position[1]+size[1]),
                (position[0], position[1]+size[1])
            ]
        else:
            print("Position and size must be at least 2-tuple")
            raise Exception

    '''
    Renderer 2D
    '''

    def clearAll(self, clearColor=None):
        self._game._mainCanvas.delete("all")
        color = self.getColor()
        if clearColor is None:
            self.setColor(self.getBackground())
        else:
            self.setColor(clearColor)
        self.fillRect((0, 0), self._game.getSize())
        self.setColor(color)

    def setLayer(self, obj, layer):
        if layer > 0:
            # Higher should be more visible
            self._game._mainCanvas.tag_lower(obj, layer)

    def drawArc(self, position, size, start=0, end=360):
        self.fillArc(position, size, start, end, "")

    def drawImage(self, image, position):
        self._game._mainCanvas

    def drawLine(self, coords, cap=tk.BUTT, join=tk.ROUND, roundness=0):
        if self._isOutside(self._getPosition(coords)):
            return None
        self._game._mainCanvas.create_line(
            self._toCoord(
                self._getPosition(coords)
            ), fill=self._fgColor, smooth=roundness, width=self._strokeSize,
            capstyle=cap, joinstyle=join
        )

    def drawOval(self, position, size):
        self.fillOval(position, size, "")

    def drawPoint(self, position):
        self.fillRect(position, [1, 1])

    def drawPolygon(self, coords, roundness=0):
        self.fillPolygon(coords, roundness, "")

    def drawRect(self, position, size):
        self.fillRect(position, size, "")

    def drawRoundRect(self, position, size, roundness):
        self.fillRoundRect(position, size, roundness, "")

    def drawString(self, position, string, anchor=tk.NW, align=tk.LEFT,
                   width=None):
        self._game._mainCanvas.create_text(
            position[0], position[1], fill=self._fgColor, width=width,
            text=string, anchor=anchor, justify=align
        )

    def fillArc(self, position, size, start=0, end=360, fill=None):
        if self._isOutside(
            self._getPosition(self._toRectCoord(position, size))
        ):
            return None
        if fill is None:
            fill = self._fgColor
        start += 180
        end += 180
        self._game._mainCanvas.create_arc(
            position[0], position[1], position[0]+size[0], position[1]+size[1],
            outline=self._fgColor, fill=fill, width=self._strokeSize,
            style=tk.ARC, start=start, extent=start-end
        )

    def fillOval(self, position, size, fill=None):
        if self._isOutside(
            self._getPosition(self._toOvalCoord(position, size))
        ):
            return None
        if fill is None:
            fill = self._fgColor
        self._game._mainCanvas.create_oval(
            position[0]-(size[0]/2), position[1]-(size[1]/2),
            position[0]+(size[0]/2), position[1]+(size[1]/2),
            outline=self._fgColor, fill=fill, width=self._strokeSize
        )

    def fillPolygon(self, coords, roundness=0, fill=None):
        if self._isOutside(self._getPosition(coords)):
            return None
        if fill is None:
            fill = self._fgColor
        self._game._mainCanvas.create_polygon(
            self._toCoord(self._getPosition(coords)), outline=self._fgColor,
            fill=fill, smooth=roundness, width=self._strokeSize
        )

    def fillRect(self, position, size, fill=None):
        self.fillRoundRect(position, size, 0, fill)

    def fillRoundRect(self, position, size, roundness=0, fill=None):
        self.fillPolygon(self._toRectCoord(position, size), roundness, fill)

    def getColor(self):
        return self._fgColor

    def setColor(self, color):
        self._fgColor = color

    def getBackground(self):
        return self._bgColor

    def setBackground(self, color):
        self._bgColor = color

    '''
    Renderer 3D
    '''

    def getPreOffset(self):
        return self._render3d._preOffset

    def setPreOffset(self, offset):
        self._render3d._preOffset = offset

    def addPostOffset(self, offset):
        self._render3d._preOffset = self._render3d._preOffset+offset

    def getPostOffset(self):
        return self._render3d._postOffset

    def setPostOffset(self, offset):
        self._render3d._postOffset = offset

    def setPerspective(self, perspective):
        if isinstance(perspective, int) or isinstance(perspective, float):
            self.setPerspective((perspective, perspective, 0.5, 0.5))
            return
        for per in perspective:
            if per == 0:
                print("Perspective must not be zero")
                return
        self._render3d._perspective = perspective

    def getPerspectiveX(self):
        return self._render3d._perspective[0]

    def getPerspectiveY(self):
        return self._render3d._perspective[1]

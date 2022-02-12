from drawable import Drawable
import window
import conf
from cell import Cell
from label import Label


class Board(Drawable):
    activeCellNr = None

    def __init__(self, pos, size, arr, bg=conf.bgColor, fg=conf.fgColor):
        super().__init__(pos, size, bg, fg)
        self.arr = arr
        self.idx = 0
        self.lblLevel = Label("---", (0, 0), (1, 1))
        self.lblMove = Label("---", (0, 0), (1, 1))
        self.lblLives = Label("---", (0, 0), (1, 1))
        self.field = self.createField(size[0], size[1])
        self._bgColor = conf.bgColor
        if not conf.feedbackOnPreviousMove:
            self.lblMove.visible = False
            self.lblLives.visible = False
        if conf.manualMode:
            self.lblLives.visible = False
        self.resize(pos, size)

    def createField(self, w, h):
        size = conf.fieldSize
        cellSize = h/(size+1)
        marginX = w/2 - (cellSize*size)/2
        marginY = h/2 - (cellSize*size)/2
        field = []
        for y in range(size):
            for x in range(size):
                isCenter = False
                cellX = x*cellSize+marginX
                cellY = y*cellSize+marginY
                if size//2 == x and size//2 == y:
                    isCenter = True
                c = Cell((cellX, cellY), (cellSize, cellSize), isCenter)
                field.append(c)
        return field

    def isCellActive(self):
        return self.field[self.activeCellNr].active == True

    def cellOn(self):
        self.lastActiveCellNr = self.activeCellNr
        self.field[self.activeCellNr].active = True

    def cellOff(self):
        self.field[self.activeCellNr].active = False

    def setNewActiveCell(self):
        self.lastActiveCellNr = self.activeCellNr
        self.getNextActiveCell()

    def getNextActiveCell(self):
        self.activeCellNr = self.arr[self.idx]
        self.idx += 1

    @property
    def bgColor(self):
        return self._bgColor

    @bgColor.setter
    def bgColor(self, color):
        self._bgColor = color
        self.lblMove.bg = self._bgColor
        self.lblLives.bg = self._bgColor
        self.lblLevel.bg = self._bgColor
        for _, cell in enumerate(self.field):
            cell.bg = self._bgColor

    def update(self, dt):
        for cell in self.field:
            cell.update(dt)
        self.lblLevel.update(dt)
        self.lblLives.update(dt)
        self.lblMove.update(dt)

    def draw(self, screen):
        self.lblLevel.draw(screen)
        self.lblMove.draw(screen)
        self.lblLives.draw(screen)
        for cell in self.field:
            cell.draw(screen)

    def resize(self, pos, size):
        super().resize(pos, size)
        w, h = size
        wW, hH = int(w*0.3), int(h*0.08)
        self.lblLevel.resize((0, 0), (wW, hH))
        self.lblMove.resize((window.rect.w-wW, 0), (wW, hH))
        self.lblLives.resize((window.rect.w/2-wW/2, 0), (wW, hH))
        dim = conf.fieldSize
        wSize = h if w > h else w
        cellSize = wSize/(dim+1)
        marginX = w/2 - (cellSize*dim)/2
        marginY = h/2 - (cellSize*dim)/2
        for i, cell in enumerate(self.field):
            x = i % dim
            y = i//dim
            cellX = x*cellSize+marginX
            cellY = y*cellSize+marginY
            cell.resize([cellX, cellY], [cellSize, cellSize])

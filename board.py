import window
import conf
from cell import Cell
from label import Label


class Board:
    activeCellNr = None

    def __init__(self, arr) -> None:
        self.arr = arr
        self.idx = 0
        w, h = int(window.rect.w*0.3), int(window.rect.h*0.08)
        self.lblLevel = Label("---", (0, 0), (w, h))
        self.lblMove = Label("---", (window.rect.w-w, 0), (w, h))
        self.lblLives = Label("---", (window.rect.w/2-w/2, 0), (w, h))
        self.field = self.createField(window.rect.w, window.rect.h)
        self.bgColor = conf.bgColor
        if not conf.feedbackOnPreviousMove:
            self.lblMove.visible = False
            self.lblLives.visible = False

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

    def setBgColor(self, color):
        self.bgColor = color
        self.lblMove.bg = self.bgColor
        self.lblLives.bg = self.bgColor
        self.lblLevel.bg = self.bgColor
        for _, cell in enumerate(self.field):
            cell.bg = self.bgColor

    def update(self, dt):
        for cell in self.field:
            cell.update(dt)
        self.lblLevel.update(dt)
        self.lblLives.update(dt)
        self.lblMove.update(dt)

    def draw(self, screen):
        self.lblLevel.draw(screen)
        self.lblMove.draw(screen)
        if not conf.manualMode:
            self.lblLives.draw(screen)
        for cell in self.field:
            cell.draw(screen)

    def resize(self):
        w, h = window.rect.w, window.rect.h
        size = conf.fieldSize
        wSize = h if w > h else w
        cellSize = wSize/(size+1)
        marginX = w/2 - (cellSize*size)/2
        marginY = h/2 - (cellSize*size)/2
        for i, cell in enumerate(self.field):
            x = i % size
            y = i//size
            cellX = x*cellSize+marginX
            cellY = y*cellSize+marginY
            cell.resize([cellX, cellY], [cellSize, cellSize])
        w, h = int(window.rect.w*0.3), int(window.rect.h*0.08)
        self.lblLevel.resize((0, 0), (w, h))
        self.lblMove.resize((window.rect.w-w, 0), (w, h))
        self.lblLives.resize((window.rect.w/2-w/2, 0), (w, h))

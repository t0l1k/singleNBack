import random
import conf
from cell import Cell
from label import Label


class Board:
    activeCellNr = None

    def __init__(self) -> None:
        self.field = self.createField(conf.w, conf.h)
        w, h = int(conf.w*0.2), int(conf.h*0.1)
        x = conf.w/2-w/2
        y = conf.h/2-h/2
        self.lblLevel = Label("---", (0, 0), (w, h))
        self.lblMove = Label("---", (conf.w-w, 0), (w, h))
        self.lblLives = Label("---", (conf.w/2-w/2, 0), (w, h))

    def createField(self, w, h):
        size = conf.fieldSize
        cellSize = h/(size+1)
        marginX = w/2 - (cellSize*size)/2
        marginY = h/2 - (cellSize*size)/2
        field = []
        for y in range(size):
            for x in range(size):
                cellX = x*cellSize+marginX
                cellY = y*cellSize+marginY
                c = Cell((cellX, cellY), cellSize)
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
        self.activeCellNr = random.randint(0, len(self.field)-1)

    def draw(self, screen):
        self.lblLevel.draw(screen)
        self.lblMove.draw(screen)
        if not conf.manualMode:
            self.lblLives.draw(screen)
        for cell in self.field:
            cell.draw(screen)

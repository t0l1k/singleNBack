import pygame
import conf
from board import Board


class GameLogic:
    # Классический nback, есть поле 3х3 в нем появляются иконки и при повторе n-шагов назад отметить повтор, после завершения сессии выдать результат, при проценте выше 80 переход на следующий уровень, при проценте ниже 50 повтор этого же уровня в три попытки, если попытки исчерпаны, переход на уровень ниже.

    def __init__(self) -> None:
        self.timeToNextCell = conf.timeToNextCell
        self.timeCellShow = conf.timeShowCell
        self.delayBeforeShow = ((conf.timeToNextCell-conf.timeShowCell)/2)
        self.moves = []
        self.board = Board()
        self.bgColor = conf.bgColor
        self.level = conf.beginLevel

    def start(self):
        self.inGame = True
        self.resetLevel = False
        self.sessionTimer = self.getTick()
        self.move = self.setLevelMoveCount(self.level)
        self.lives = conf.lives
        self.msg = "Game started"
        self.msgTimer = ""
        self.pressed = False
        self.pauseTime = conf.timePause * 1000
        self.resetNewCellTimer()
        self.board.setNewActiveCell()
        self.board.cellOff()

    def resetNewCellTimer(self):
        self.beginNewCell = self.getTick()-self.delayBeforeShow
        self.delayEnd = self.beginNewCell+self.delayBeforeShow

    def setLevelMoveCount(self, level):
        conf.maxMoves = conf.moves*level+level+1
        return conf.maxMoves

    def keyPress(self):
        self.pressed = True
        self.bgColor = conf.blue

    def checkLastMove(self):
        pass

    def update(self):
        self.gameTimer = self.getTick()-self.sessionTimer
        if self.inGame:
            if self.getTick()-self.beginNewCell > self.timeToNextCell:  # показать новую клетку
                self.move -= 1
                self.moves.append(self.board.activeCellNr)
                self.board.cellOff()
                self.resetNewCellTimer()
                self.board.setNewActiveCell()
                self.bgColor = conf.bgColor
            if self.getTick()-self.beginNewCell < self.timeToNextCell:  # во время показа новой иконки
                if self.getTick() > self.delayBeforeShow+self.delayEnd and not self.board.isCellActive():  # время показать новую иконку
                    self.checkLastMove()
                    self.board.cellOn()
                if self.move < 1:
                    self.move = 0
                    self.board.cellOff()
                    self.inGame = False
        else:
            pass
        self.setLabels()

    def setLabels(self):
        self.board.lblLevel.setText("N-Back "+str(self.level))
        self.board.lblMove.setText(str(self.move))
        self.board.lblTimer.setText(str(self.gameTimer//1000))
        self.board.lblLives.setText("Lives: "+str(self.lives))
        self.board.lblPauseNextLevel.setText(
            self.msg+" уровень:"+str(self.level))
        self.board.lblPauseTimer.setText(self.msgTimer)

    def draw(self, screen):
        screen.fill(self.bgColor)
        self.board.draw(screen)

    def getTick(self):
        return pygame.time.get_ticks()

    def quit(self):
        pass

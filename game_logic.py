import pygame
import conf
from board import Board


class GameLogic:
    # Классический nback, есть поле 3х3 в нем появляются иконки и при повторе n-шагов назад отметить повтор, после завершения сессии выдать результат, при проценте выше 80 переход на следующий уровень, при проценте ниже 50 повтор этого же уровня в три попытки, если попытки исчерпаны, переход на уровень ниже.

    def __init__(self) -> None:
        self.board = Board()
        self.bgColor = conf.bgColor
        self.level = conf.beginLevel
        self.move = self.setLevelMoveCount(self.level)

    def start(self):
        self.sessionTimer = self.getTick()
        self.lives = conf.lives
        self.msg = "Game started"
        self.msgTimer = ""

    def setLevelMoveCount(self, level):
        conf.maxMoves = conf.moves*level+level
        return conf.maxMoves

    def keyPress(self):
        pass

    def update(self):
        self.gameTimer = self.getTick()-self.sessionTimer

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

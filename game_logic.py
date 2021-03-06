import datetime
import pygame
import conf
from board import Board
import logging
from drawable import Drawable
from gamedata import GameData


log = logging.getLogger(__name__)


class GameLogic(Drawable):
    # Классический nback, есть поле 3х3 в нем появляются иконки и при повторе n-шагов назад отметить повтор, после завершения сессии выдать результат, при проценте выше 80 переход на следующий уровень, при проценте ниже 50 повтор этого же уровня в три попытки, если попытки исчерпаны, переход на уровень ниже.
    def __init__(self, pos, size, count=0, level=1, lives=0, arr=None, bg=conf.bgColor, fg=conf.fgColor):
        super().__init__(pos, size, bg, fg)
        self.gameCount = count
        self.level = level
        self.lives = lives
        self.board = Board(pos, size, arr)

    def start(self):
        self.inGame = True
        self.moves = []
        self.moveCount = getTotalMoves(self.level)
        self.pressed = False
        self.board.setNewActiveCell()
        self.board.cellOff()
        self.bgColor = conf.bgColor
        self.countCorrect = 0
        self.countWrong = 0
        self.resetLevel = False
        self.resetNewCellTimer()
        self.beginTime = datetime.datetime.now()

    def resetNewCellTimer(self):
        self.timeToNextCell = conf.timeToNextCell
        self.timeCellShow = conf.timeShowCell
        if self.lives < conf.thresholdFallbackSessions:
            step = (conf.thresholdFallbackSessions -
                    self.lives)*conf.incDurrationStep
            self.timeToNextCell += step
            self.timeCellShow += step
        self.delayBeforeShow = ((self.timeToNextCell-self.timeCellShow)/2)
        self.beginNewCell = self.getTick()-self.delayBeforeShow
        self.delayEnd = self.beginNewCell+self.delayBeforeShow
        self.lastTimeToNextCellCheck = self.getTick()

    def keyPressed(self):
        self.pressed = True
        if conf.feedbackOnPreviousMove:
            self.bgColor = conf.regularColor

    def checkLastMove(self):
        if len(self.moves) > self.level:
            # уже есть что анализировать на правильный ход
            s = "#{} nB{} ход:{} {} {}-{}".format(self.gameCount, self.level, getTotalMoves(self.level)-self.moveCount, self.moves[len(
                self.moves)-self.level-1:len(self.moves)], self.board.lastActiveCellNr, self.moves[len(self.moves)-1-self.level])
            log.debug(s+" пауза:%s", self.timeToNextCell)
            if self.moves[len(self.moves)-1-self.level] == self.board.lastActiveCellNr:
                # есть повтор n-шагов назад
                if self.pressed:  # правильный ответ
                    self.countCorrect += 1
                    if conf.feedbackOnPreviousMove:
                        self.bgColor = conf.correctColor
                    log.debug("правильный ответ")
                else:  # пропустили правильный ответ
                    self.countWrong += 1
                    if conf.feedbackOnPreviousMove:
                        self.bgColor = conf.errorColor
                    log.debug("пропустили ответ")
            elif self.pressed:  # определен повтор неправильно
                self.countWrong += 1
                if conf.feedbackOnPreviousMove:
                    self.bgColor = conf.warningColor
                log.debug("не было повтора")
        elif self.pressed:  # еще не могло быть повтора
            self.countWrong += 1
            if conf.feedbackOnPreviousMove:
                self.bgColor = conf.warningColor
            log.debug("не было повтора")
        if self.countWrong > 0 and conf.resetLevelOnFirstWrong:
            self.resetLevel = True
        self.pressed = False

    def update(self, dt):
        if self.inGame:
            if self.getTick()-self.lastTimeToNextCellCheck > self.timeToNextCell:
                # показать новую клетку
                self.moveCount -= 1
                self.moves.append(self.board.activeCellNr)
                self.board.cellOff()
                self.resetNewCellTimer()
                if self.moveCount > 0:
                    self.board.setNewActiveCell()
                if conf.feedbackOnPreviousMove:
                    self.bgColor = conf.bgColor
                self.lastTimeToNextCellCheck = self.getTick()
            if self.getTick()-self.beginNewCell < self.timeToNextCell:
                # во время показа новой иконки
                if self.getTick() > self.delayBeforeShow+self.delayEnd and not self.board.isCellActive():
                    log.debug("время для новой клетки")
                    self.checkLastMove()
                    self.board.cellOn()
                    if self.moveCount <= 0 or self.resetLevel:  # переход на следующий уровень
                        log.debug("игра окончена")
                        self.board.cellOff()
                        self.inGame = False
            if len(self.moves) < self.level:  # цвет фона regular пока нет ходов для анализа
                self.bgColor = conf.regularColor
            self.board.update(dt)
        self.setLabels()

    def getTick(self):
        return pygame.time.get_ticks()

    def sendGameResult(self):
        log.info("узнать результаты игры")
        return GameData(
            self.level,
            self.lives,
            getTotalMoves(self.level) - self.moveCount,
            self.countCorrect, self.countWrong,
            self.getPercent(),
            True,
            dateBegin=self.beginTime,
            dateEnd=datetime.datetime.now(),
            field=self.board.arr)

    def getPercent(self):
        if self.resetLevel:
            return 0
        aa = self.countCorrect
        bb = self.countWrong
        if aa == 0 and bb == 0:
            a, b = 1, 0
        elif aa == 0 and bb > 0:
            a, b = 0, 1
        else:
            a, b = aa, bb
        return int(a*100/(a+b))

    def setLabels(self):
        self.board.bgColor = self.bgColor
        self.board.lblLevel.text = "#" + \
            str(self.gameCount)+" N-Back " + \
            str(self.level)+" " + "\u2665"*self.lives
        self.board.lblMove.text = str(self.moveCount)

    def draw(self, screen):
        screen.fill(self.bgColor)
        self.board.draw(screen)

    def resize(self, pos, size):
        super().resize(pos, size)
        self.board.resize(pos, size)


def getTotalMoves(level):
    return conf.numTrials+conf.numTrialsFactor*level**conf.numTrialsExponent

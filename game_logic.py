import datetime
import random
import pygame
import conf
from board import Board
import logging as log
import time
from today_games_data import GameData


class GameLogic:
    # Классический nback, есть поле 3х3 в нем появляются иконки и при повторе n-шагов назад отметить повтор, после завершения сессии выдать результат, при проценте выше 80 переход на следующий уровень, при проценте ниже 50 повтор этого же уровня в три попытки, если попытки исчерпаны, переход на уровень ниже.

    def __init__(self, count, level, lives) -> None:
        self.gameCount = count
        self.level = level
        self.lives = lives
        self.board = Board(self.getArr())

    def start(self):
        self.inGame = True
        self.moves = []
        self.moveCount = self.getTotalMoves()
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
        if self.lives < conf.lives:
            step = (conf.lives-self.lives)*conf.incDurrationStep
            self.timeToNextCell += step
            self.timeCellShow += step
        self.delayBeforeShow = ((self.timeToNextCell-self.timeCellShow)/2)
        self.beginNewCell = self.getTick()-self.delayBeforeShow
        self.delayEnd = self.beginNewCell+self.delayBeforeShow
        self.lastTimeToNextCellCheck = self.getTick()

    def getTotalMoves(self):
        # вычислить число ходов на основе константы maxMoves
        return conf.moves*self.level+self.level

    def keyPressed(self):
        self.pressed = True
        if conf.feedbackOnPreviousMove:
            self.bgColor = conf.regularColor

    def checkLastMove(self):
        if len(self.moves) > self.level:
            # уже есть что анализировать на правильный ход
            s = "#{} nB{} ход:{} {} {}-{}".format(self.gameCount, self.level, self.getTotalMoves()-self.moveCount, self.moves[len(
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

    def update(self):
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
        self.setLabels()

    def sendGameResult(self):
        log.info("узнать результаты игры")
        return GameData(
            self.level,
            self.lives,
            self.getTotalMoves() - self.moveCount,
            self.countCorrect, self.countWrong,
            self.getPercent(),
            True,
            dateBegin=self.beginTime,
            dateEnd=datetime.datetime.now())

    def getPercent(self):
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
        self.board.lblLevel.setText(
            "#"+str(self.gameCount)+" N-Back "+str(self.level))
        self.board.lblMove.setText(str(self.moveCount))
        self.board.lblLives.setText("Lives: "+str(self.lives))

    def draw(self, screen):
        screen.fill(self.bgColor)
        self.board.draw(screen)

    def getTick(self):
        return pygame.time.get_ticks()

    def resize(self):
        self.board.resize()

    def getNextArr(self):
        arr = []
        while(len(arr) < self.getTotalMoves()):
            arr.append(random.randint(0, (conf.fieldSize*conf.fieldSize)-1))
        return arr

    def checkRandomRepition(self, arr):
        count = 0
        for i, v in enumerate(arr):
            nextMove = i+self.level
            if nextMove > len(arr)-1:
                break
            if v == arr[nextMove]:
                count += 1
        percent = int(100*count/len(arr))
        return percent > conf.RR and percent < 80, percent

    def getArr(self):
        pause = conf.timeoutRR
        start = time.monotonic()
        count = 0
        check = False
        max = 0
        best = []
        while count < 100000 and time.monotonic()-start < pause and not check:
            arr = self.getNextArr()
            check, percent = self.checkRandomRepition(arr)
            if percent > max:
                max = percent
                best = arr
            count += 1
        if not check:
            log.info("Game selected with RR:%s", max)
            return best
        log.info("Game selected with RR:%s", percent)
        return arr

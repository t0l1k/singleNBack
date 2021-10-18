import pygame
import conf
import datetime
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
        self.countCorrect = 0
        self.countWrong = 0
        self.gameAverage = 0
        self.gameCount = 0
        self.games = {}
        self.max = conf.beginLevel
        self.lastTimeToNextCellCheck = self.getTick()

    def resetNewCellTimer(self):
        self.beginNewCell = self.getTick()-self.delayBeforeShow
        self.delayEnd = self.beginNewCell+self.delayBeforeShow

    def setLevelMoveCount(self, level):
        conf.maxMoves = conf.moves*level+level+1
        return conf.maxMoves

    def keyPressed(self):
        self.pressed = True
        self.bgColor = conf.blue

    def checkLastMove(self):
        if len(self.moves) > self.level:  # есть что анализировать на правильный ход
            print(
                "#"+str(self.gameCount),
                "nB"+str(self.level),
                "ход:", conf.maxMoves-self.move,
                self.moves[len(self.moves)-self.level-1:len(self.moves)],
                self.board.lastActiveCellNr,
                self.moves[len(self.moves)-1-self.level])
            # есть повтор n-шагов назад
            if self.moves[len(self.moves)-1-self.level] == self.board.lastActiveCellNr:
                if self.pressed:  # правильный ответ
                    self.countCorrect += 1
                    self.bgColor = conf.green
                else:  # пропустили правильный ответ
                    self.countWrong += 1
                    self.bgColor = conf.red
            elif self.pressed:  # определен повтор неправильно
                self.countWrong += 1
                self.bgColor = conf.orange
        elif self.pressed:  # еще не могло быть повтора
            self.countWrong += 1
            self.bgColor = conf.orange
        self.pressed = False

    def update(self):
        self.gameTimer = self.getTick()-self.sessionTimer
        if self.inGame:
            if self.getTick()-self.lastTimeToNextCellCheck > self.timeToNextCell:  # показать новую клетку
                self.move -= 1
                self.moves.append(self.board.activeCellNr)
                self.board.cellOff()
                self.resetNewCellTimer()
                self.board.setNewActiveCell()
                self.bgColor = conf.bgColor
                self.lastTimeToNextCellCheck = self.getTick()

            if self.getTick()-self.beginNewCell < self.timeToNextCell:  # во время показа новой иконки
                if self.getTick() > self.delayBeforeShow+self.delayEnd and not self.board.isCellActive():  # время показать новую иконку
                    self.checkLastMove()
                    self.board.cellOn()
                    if self.move < 1:  # переход на следующий уровень
                        self.gameCount += 1
                        self.pauseTimer = self.getTick()
                        self.move = 0
                        self.board.cellOff()
                        self.inGame = False
                        self.pauseTime = conf.timePause * 1000*(
                            conf.lives+1-self.lives)
                        self.levelResult = self.getLevelResultPercent(
                            self.countCorrect, self.countWrong)  # результат уровня в процентах
                        self.games[self.gameCount] = [
                            self.level, self.levelResult, datetime.datetime.now().strftime('%Y%m%d%H%M%S')]
                        self.gameAverage = self.getTodayAverage()
                        s = "#{} nBack{} правильных:{} ошибок:{} процент:{} max:{} Av:{}".format(
                            self.gameCount, self.level, self.countCorrect, self.countWrong, self.levelResult, self.max, round(self.gameAverage, 1))
                        self.msg = s
                        print(s)
                        if self.levelResult >= conf.nextLevelPercent:  # переход на следующий уровень
                            self.level += 1
                            self.lives = conf.lives
                        elif self.levelResult < conf.dropLevelPercent:  # переход на уровень ниже
                            self.lives -= 1
                            if self.lives == 0:
                                self.level -= 1
                                self.lives = conf.lives
                            if self.level <= 1:
                                self.lives = conf.lives
                        if self.max < self.level:
                            self.max = self.level
                        self.countCorrect = 0
                        self.countWrong = 0
                        self.move = self.setLevelMoveCount(self.level)
                        self.moves = []
                        self.board.lblPauseNextLevel.visible = True
                        self.board.lblPauseTimer.visible = True
        else:
            if self.getTick()-self.pauseTimer > self.pauseTime:  # пауза закончилась
                self.board.lblPauseNextLevel.visible = False
                self.board.lblPauseTimer.visible = False
                self.inGame = True
                self.pressed = False
            else:
                self.msgTimer = str(
                    self.pauseTime//1000-(self.getTick()-self.pauseTimer)//1000)
        self.setLabels()

    def getTodayAverage(self):
        result = 0
        for k, v in self.games.items():
            result += v[0]
        return result/len(self.games)

    def getLevelResultPercent(self, aa, bb):
        if aa == 0 and bb == 0:
            a, b = 1, 0
        elif aa == 0 and bb > 0:
            a, b = 0, 1
        else:
            a, b = aa, bb
        return int(a*100/(a+b))

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
        for k, v in self.games.items():
            print("#"+str(k), "A"+str(v[0])+"B", v[1], v[2])
        s = "Play Time {}m{}s max:{} Av:{}".format(
            self.gameTimer//1000//60, self.gameTimer//1000 % 60,
            self.max, self.gameAverage)
        print(s)

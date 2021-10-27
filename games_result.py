import pygame
import conf
from label import Label
import logging as log


class GameResults:
    def __init__(self) -> None:
        self.inGame = False
        self.bgColor = conf.bgColor
        self.pauseTime = conf.timePause*1000
        self.pauseTimer = pygame.time.get_ticks()
        self.setupScene()

    def setupScene(self):
        w, h = int(conf.w*0.2), int(conf.h*0.07)
        self.lblName = Label("Results", (0, 0), (w, h), bg=self.bgColor)
        w = int(conf.w*0.95)
        x = conf.w/2-w/2
        y = conf.h/2-h/2
        self.lblResults = Label("---", (x, y), (w, h), bg=self.bgColor)
        w, h = int(conf.w*0.3), int(conf.h*0.3)
        x = conf.w/2-w/2
        y = conf.h/4-h/2
        self.lblTimer = Label("---", (x, y), (w, h), bg=self.bgColor)

    def getGameResult(self, count):
        self.level = conf.todayGamesData[count][0]
        correct, wrong = conf.todayGamesData[count][1], conf.todayGamesData[count][2]
        self.lives = conf.todayGamesData[count][3]
        self.percent = conf.todayGamesData[count][5]
        s = "#{} Уровень:{} процент:{} правильных:{} ошибок:{}".format(
            count, self.level, self.percent, correct, wrong)
        self.lblResults.setText(s)
        self.lblTimer.visible = True
        self.pauseTime = (conf.lives + 1 - self.lives) * conf.timePause*1000
        self.pauseTimer = pygame.time.get_ticks()
        self.lblName.setBgColor(self.bgColor)
        self.lblResults.setBgColor(self.bgColor)
        self.lblTimer.setBgColor(self.bgColor)
        log.debug(s)

    def update(self):
        if self.inGame:
            if self.isPaused():
                self.lblTimer.visible = False
            else:
                self.lblTimer.setText(
                    str(self.pauseTime//1000-(pygame.time.get_ticks()-self.pauseTimer)//1000))

    def isPaused(self):
        return pygame.time.get_ticks()-self.pauseTimer > self.pauseTime

    def draw(self, screen):
        screen.fill(self.bgColor)
        self.lblName.draw(screen)
        self.lblResults.draw(screen)
        self.lblTimer.draw(screen)

    def keyPressed(self):
        if not self.isPaused():
            return False
        log.info("Запустить новую игру")
        return True

    def quit(self):
        log.info("Выход со сцены результатов")
        return True

    def resize(self):
        w, h = int(conf.w*0.2), int(conf.h*0.08)
        self.lblName.resize((0, 0), (w, h))
        w = int(conf.w*0.95)
        x = conf.w/2-w/2
        y = conf.h/2-h/2
        self.lblResults.resize((x, y), (w, h))
        w, h = int(conf.w*0.3), int(conf.h*0.3)
        x = conf.w/2-w/2
        y = conf.h/4-h/2
        self.lblTimer.resize((x, y), (w, h))

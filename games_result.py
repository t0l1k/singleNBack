import pygame
import scene
import conf
import today_games_data
from label import Label
import logging

log = logging.getLogger(__name__)


class GameResults:
    def __init__(self) -> None:
        self.inGame = False
        self.bgColor = conf.bgColor
        self.pauseTime = conf.timePause*1000
        self.pauseTimer = pygame.time.get_ticks()

        self.lblName = Label("Results", (0, 0), (1, 1), bg=self.bgColor)
        self.lblResults = Label("---", (0, 0), (1, 1), bg=self.bgColor)
        self.lblTimer = Label("---", (0, 0), (1, 1), bg=self.bgColor)
        self.resize()

    def setup(self, color):
        self.bgColor = color
        s = today_games_data.getDoneGamesStr()
        self.lblResults.text = s
        log.debug(s)
        self.lblTimer.visible = True
        lives = today_games_data.getLivesFromGame(
            today_games_data.getGameCount())
        self.pauseTime = (conf.lives + 1 - lives) * conf.timePause*1000
        self.pauseTimer = pygame.time.get_ticks()
        self.lblName.bg = self.bgColor
        self.lblResults.bg = self.bgColor
        self.lblTimer.bg = self.bgColor
        self.inGame = True

    def update(self):
        if self.inGame:
            if self.isPaused():
                if self.lblTimer.visible:
                    self.lblTimer.visible = False
                    if not conf.autoToNextLevel:
                        scene.pop()
            else:
                self.lblTimer.text = str(
                    self.pauseTime//1000-(pygame.time.get_ticks()-self.pauseTimer)//1000)

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

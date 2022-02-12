import pygame
from drawable import Drawable
import scene
import conf
import today_games_data
from label import Label
import logging

log = logging.getLogger(__name__)


class GameResult(Drawable):
    def __init__(self, pos, size, bg=conf.bgColor, fg=conf.fgColor):
        super().__init__(pos, size, bg, fg)
        self.inGame = False
        self.bgColor = bg
        self.pauseTime = conf.timePause*1000
        self.pauseTimer = pygame.time.get_ticks()
        self.lblName = Label("Result", (0, 0), (1, 1), bg=self.bgColor)
        self.lblResults = Label("---", (0, 0), (1, 1), bg=self.bgColor)
        self.lblTimer = Label("---", (0, 0), (1, 1), bg=self.bgColor)
        self.resize(pos, size)

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

    def update(self, dt):
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

    def draw(self, surface):
        surface.fill(self.bgColor)
        self.lblName.draw(surface)
        self.lblResults.draw(surface)
        self.lblTimer.draw(surface)

    def keyPressed(self):
        if not self.isPaused():
            return False
        log.info("Запустить новую игру")
        return True

    def quit(self):
        log.info("Выход со сцены результатов")
        return True

    def resize(self, pos, size):
        super().resize(pos, size)
        w, h = int(size[0]*0.2), int(size[1]*0.08)
        self.lblName.resize((0, 0), (w, h))
        w = int(size[0]*0.95)
        x = size[0]/2-w/2
        y = size[1]/2-h/2
        self.lblResults.resize((x, y), (w, h))
        w, h = int(size[0]*0.3), int(size[1]*0.3)
        x = size[0]/2-w/2
        y = size[1]/4-h/2
        self.lblTimer.resize((x, y), (w, h))

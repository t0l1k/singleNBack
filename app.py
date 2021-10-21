from scene_today import SceneToday
from scene_game import SceneGame
from label import Label
import conf
import pygame
import logging as log


class App:
    def __init__(self) -> None:
        self.sceneToday = SceneToday(self)
        self.sceneGame = SceneGame(self)
        self.currentScene = self.sceneToday
        w, h = int(conf.w*0.2), int(conf.h*0.1)
        self.lblTimer = Label("---", (conf.w/2-w/2, conf.h-h), (w, h))
        self.sessionTimer = pygame.time.get_ticks()

    def setSceneToday(self):
        self.sceneToday.setScene(None)
        self.currentScene = self.sceneToday
        log.debug("set Scene Today")

    def setSceneGame(self):
        self.sceneGame.setScene(self.sceneToday)
        self.currentScene = self.sceneGame
        log.debug("set Scene Game")

    def update(self):
        self.gameTimer = pygame.time.get_ticks()-self.sessionTimer
        self.currentScene.update()
        timeStr = "{:>02}:{:>02}".format(
            self.gameTimer//1000//60, self.gameTimer//1000 % 60)
        self.lblTimer.setText(timeStr)

    def draw(self, screen):
        self.currentScene.draw(screen)
        self.lblTimer.draw(screen)

    def keyPressed(self):
        log.debug("space pressed in app")
        self.currentScene.keyPressed()

    def quitScene(self):
        log.debug("quit scene in app")
        if self.currentScene.next is None:
            self.currentScene.quit()
            return True
        else:
            self.currentScene.quit()
            return False

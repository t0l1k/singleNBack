import conf
import logging as log
from scene_today import SceneToday
from scene_game import SceneGame
from label import Label
from scene_game_timer import Timer


class App:
    def __init__(self) -> None:
        self.sceneToday = SceneToday(self)
        self.sceneGame = SceneGame(self)
        self.currentScene = self.sceneToday
        w, h = int(conf.w*0.2), int(conf.h*0.1)
        self.lblTimer = Label("---", (conf.w/2-w/2, conf.h-h), (w, h))
        self.sessionTimer = Timer()
        self.sessionTimer.start()

    def setSceneToday(self):
        self.sceneToday.setScene(None)
        self.currentScene = self.sceneToday
        log.info("set Scene Today")

    def setSceneGame(self):
        self.sceneGame.setScene(self.sceneToday)
        self.currentScene = self.sceneGame
        log.info("set Scene Game")

    def update(self):
        self.currentScene.update()
        self.lblTimer.setText(self.sessionTimer.__str__())

    def draw(self, screen):
        self.currentScene.draw(screen)
        self.lblTimer.draw(screen)

    def keyPressed(self):
        log.info("space pressed in app")
        self.currentScene.keyPressed()

    def quitScene(self):
        log.info("quit scene in app")
        if self.currentScene.next is None:
            self.currentScene.quit()
            return True
        else:
            self.currentScene.quit()
            return False

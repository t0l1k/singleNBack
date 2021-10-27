import logging as log
from scene_today import SceneToday
from scene_game import SceneGame


class App:
    def __init__(self) -> None:
        self.sceneToday = SceneToday(self)
        self.sceneGame = SceneGame(self)
        self.currentScene = self.sceneToday

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

    def draw(self, screen):
        self.currentScene.draw(screen)

    def keyUp(self):
        self.currentScene.keyUp()

    def keyDown(self):
        self.currentScene.keyDown()

    def keyPressed(self):
        self.currentScene.keyPressed()

    def quitScene(self):
        if self.currentScene.next is None:
            self.currentScene.quit()
            return True
        else:
            self.currentScene.quit()
            return False

    def resize(self):
        self.sceneToday.resize()
        self.sceneGame.resize()

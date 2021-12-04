import logging as log
from scene_score import SceneScore
from scene_today import SceneToday
from scene_game import SceneGame


class App:
    def __init__(self) -> None:
        self.sceneToday = SceneToday(self)
        self.sceneGame = SceneGame(self)
        self.sceneScore = SceneScore(self)
        self.currentScene = self.sceneToday
        self.setSceneToday()

    def setSceneToday(self):
        self.sceneToday.setScene(None)
        self.currentScene = self.sceneToday
        log.info("set Scene Today")

    def setSceneGame(self):
        self.sceneGame.setScene(self.sceneToday)
        self.currentScene = self.sceneGame
        log.info("set Scene Game")

    def setSceneScore(self):
        self.sceneToday.setScene(self.sceneToday)
        self.currentScene = self.sceneScore
        log.info("set Scene Score")

    def update(self):
        self.currentScene.update()

    def draw(self, screen):
        self.currentScene.draw(screen)

    def keyUp(self):
        self.currentScene.keyUp()

    def keyDown(self):
        self.currentScene.keyDown()

    def keyTurnLeft(self):
        self.currentScene.keyTurnLeft()

    def keyTurnRight(self):
        self.currentScene.keyTurnRight()

    def keyS(self):
        self.currentScene.keyS()

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
        self.sceneScore.resize()

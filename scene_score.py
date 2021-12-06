import conf
import today_games_data
from label import Label
import logging as log
from scene_today_results import ResultView


class SceneScore:
    def __init__(self, app) -> None:
        self.app = app
        self.next = app.sceneToday
        self.setupScene()

    def setupScene(self):
        self.lblName = Label("Результаты за весь период", (0, 0), (1, 1))
        self.resultsView = ResultView((0, 0), (100, 100), plot2=True)
        self.resize()

    def keyUp(self):
        pass

    def keyDown(self):
        pass

    def getScene(self):
        return self.next

    def setScene(self, next):
        self.next = next

    def update(self):
        self.resultsView.update()

    def draw(self, screen):
        screen.fill(conf.bgColor)
        self.lblName.draw(screen)
        self.resultsView.draw(screen)

    def keyTurnLeft(self):
        pass

    def keyTurnRight(self):
        pass

    def keyPressed(self):
        if today_games_data.useHistory:
            today_games_data.loadData()
        self.app.setSceneGame()

    def keyS(self):
        pass

    def quit(self):
        self.app.setSceneToday()
        return False

    def resize(self):
        w, h = int(conf.w*0.3), int(conf.h*0.1)
        self.lblName.resize((0, 0), (w, h))
        w, h = conf.w*0.9, conf.h*0.85
        x, y = (conf.w-w)/2, conf.h-h*1.05
        self.resultsView.resize((x, y), (w, h))
        log.info("Scene Score resized")

import conf
import today_games_data
from label import Label
import logging as log
from scene_today_results import ResultView


class SceneToday:
    def __init__(self, app) -> None:
        self.app = app
        self.next = None
        self.setupScene()

    def setupScene(self):
        self.lblName = Label("Игры сегодня", (0, 0), (1, 1))
        self.lblTodayGames = Label("Игры за сегодня", (0, 0), (1, 1))
        self.resultsView = ResultView((0, 0), (100, 100))
        self.historyIndex = 0
        self.historyLenght = 0
        self.getStatistic()
        self.resize()

    def getStatistic(self):
        s = today_games_data.getTodayResults()
        log.debug(s)
        self.lblTodayGames.setText(s)
        for k, v in today_games_data.get():
            log.debug("#%s [%s]", k, v.__str__())
        self.resultsView.dirty = True

    def keyUp(self):
        log.info("Up pressed")
        self.resultsView.keyUp()

    def keyDown(self):
        log.info("Down pressed")
        self.resultsView.keyDown()

    def getScene(self):
        return self.next

    def setScene(self, next):
        self.next = next
        self.getStatistic()

    def update(self):
        self.resultsView.update()

    def draw(self, screen):
        screen.fill(conf.bgColor)
        self.lblName.draw(screen)
        self.lblTodayGames.draw(screen)
        self.resultsView.draw(screen)

    def keyTurnLeft(self):
        if self.historyLenght > self.historyIndex+1:
            self.historyIndex += 1
        if self.historyIndex >= 0:
            self.historyLenght = today_games_data.readHistory(
                self.historyIndex)
        self.getStatistic()
        log.info("Выбрали дату назад %s", self.historyIndex)

    def keyTurnRight(self):
        if self.historyIndex >= 0 and self.historyLenght > 0:
            self.historyIndex -= 1
        if self.historyIndex >= 0:
            self.historyLenght = today_games_data.readHistory(
                self.historyIndex)
        else:
            today_games_data.loadData()
        self.getStatistic()
        log.info("Выбрали дату вперед %s", self.historyIndex)

    def keyPressed(self):
        if today_games_data.useHistory:
            today_games_data.loadData()
        self.app.setSceneGame()

    def keyS(self):
        self.app.setSceneScore()

    def quit(self):
        return True

    def resize(self):
        w, h = int(conf.w*0.3), int(conf.h*0.1)
        self.lblName.resize((0, 0), (w, h))
        w, h = int(conf.w*0.95), int(conf.h*0.1)
        x = conf.w/2-w/2
        y = int(h*1.1)
        self.lblTodayGames.resize((x, y), (w, h))
        w, h = conf.w*0.8, conf.h*0.75
        x, y = (conf.w-w)/2, conf.h-h*1.03
        self.resultsView.resize((x, y), (w, h))
        log.info("Scene Today resized")

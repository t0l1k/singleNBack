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
        self.resize()

    def getGames(self):
        # вычисляет средний уровень и выводит список игр и результаты
        s = "Pos: Игр:{} Max:{} Avg:{} Игровое время:{}".format(
            today_games_data.getLastDoneGame(), today_games_data.getMaxLevel(), today_games_data.getAverage(), self.app.sceneGame.sessionTimer)
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
        self.getGames()

    def update(self):
        self.resultsView.update()

    def draw(self, screen):
        screen.fill(conf.bgColor)
        self.lblName.draw(screen)
        self.lblTodayGames.draw(screen)
        self.resultsView.draw(screen)

    def keyPressed(self):
        self.app.setSceneGame()

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

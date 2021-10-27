import conf
from label import Label
import logging as log
from scene_today_results import ResultView


class SceneToday:
    def __init__(self, app) -> None:
        self.app = app
        self.next = None
        self.setupScene()

    def setupScene(self):
        w, h = int(conf.w*0.3), int(conf.h*0.1)
        self.lblName = Label("Игры сегодня", (0, 0), (w, h))
        w, h = int(conf.w*0.95), int(conf.h*0.1)
        x = conf.w/2-w/2
        y = int(h*1.1)
        self.lblTodayGames = Label("Игры за сегодня", (x, y), (w, h))
        w, h = conf.w*0.8, conf.h*0.75
        x, y = (conf.w-w)/2, conf.h-h*1.03
        self.resultsView = ResultView((x, y), (w, h))

    def getGames(self):
        # вычисляет средний уровень и выводит список игр и результаты
        max = 0
        sum = 0
        for k, v in conf.todayGamesData.items():
            level = v[0]
            if level > max:
                max = v[0]
            sum += level
        if len(conf.todayGamesData) > 0:
            average = round(sum/len(conf.todayGamesData), 2)
        else:
            average = 0
        s = "Pos: Игр:{} Max:{} Avg:{} Игровое время:{}".format(
            len(conf.todayGamesData), max, average, self.app.sceneGame.sessionTimer)
        log.debug(s)
        self.lblTodayGames.setText(s)
        for k, v in conf.todayGamesData.items():
            s = "#{} Level:{} Percent:{}".format(k, v[0], v[5])
            log.debug(s)
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

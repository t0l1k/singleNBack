import conf
from label import Label
import logging as log


class SceneToday:
    def __init__(self, app) -> None:
        self.app = app
        self.next = None
        self.name = "Игры сегодня"
        w, h = int(conf.w*0.2), int(conf.h*0.1)
        self.lblName = Label(self.name, (0, 0), (w, h))
        w, h = int(conf.w*0.95), int(conf.h*0.1)
        x = conf.w/2-w/2
        y = int(h*1.1)
        self.lblTodayGames = Label("Игры за сегодня", (x, y), (w, h))

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
            average = sum/len(conf.todayGamesData)
        else:
            average = 0
        s = "Pos: Игр:{} Max:{} Avg:{}".format(
            len(conf.todayGamesData), max, average)
        log.info(s)
        self.lblTodayGames.setText(s)
        for k, v in conf.todayGamesData.items():
            s = "#{} Level:{} Percent:{}".format(k, v[0], v[5])
            log.info(s)

    def getScene(self):
        return self.next

    def setScene(self, next):
        self.next = next

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(conf.green)
        self.lblName.draw(screen)
        self.lblTodayGames.draw(screen)

    def keyPressed(self):
        log.debug("space pressed in sceneToday")
        self.app.setSceneGame()

    def quit(self):
        log.debug("quit in sceneToday")
        return True

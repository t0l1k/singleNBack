import conf
from label import Label
import logging as log


class GameResults:
    def __init__(self) -> None:
        self.inGame = False
        w, h = int(conf.w*0.2), int(conf.h*0.1)
        self.lblName = Label("Results", (0, 0), (w, h))
        w, h = int(conf.w*0.95), int(conf.h*0.1)
        x = conf.w/2-w/2
        y = conf.h/2-h/2
        self.lblResults = Label("---", (x, y), (w, h))
        self.bgColor = conf.gray

    def getGameResult(self, count):
        self.level = conf.todayGamesData[count][0]
        correct, wrong = conf.todayGamesData[count][1], conf.todayGamesData[count][2]
        self.lives = conf.todayGamesData[count][3]
        self.percent = conf.todayGamesData[count][5]
        s = "#{} Уровень:{} процент:{} правильных:{} ошибок:{}".format(
            count, self.level, self.percent, correct, wrong)
        self.lblResults.setText(s)
        log.info(s)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(self.bgColor)
        self.lblName.draw(screen)
        self.lblResults.draw(screen)

    def keyPressed(self):
        log.debug("Запустить новую игру")
        return True

    def quit(self):
        log.debug("quit in game results")
        return True

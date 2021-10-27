import conf
import logging as log
from game_logic import GameLogic
from games_result import GameResults
from label import Label
from scene_game_timer import Timer


class SceneGame:
    def __init__(self, app) -> None:
        self.app = app
        self.next = app.sceneToday
        self.sessionTimer = Timer()
        self.sessionTimer.start()
        self.gameCount = len(conf.todayGamesData)  # узнать номер игры
        self.setupTimerLabel()
        self.game = None

    def setupTimerLabel(self):
        w, h = int(conf.w*0.2), int(conf.h*0.08)
        self.lblTimer = Label("---", (conf.w/2-w/2, conf.h-h), (w, h))

    def getScene(self):
        return self.next

    def setScene(self, next):
        self.next = next
        if len(conf.todayGamesData) > 0:  # загрузить последний уровень и попытки
            last = len(conf.todayGamesData)-1
            self.gameStart(
                conf.todayGamesData[last][0], conf.todayGamesData[last][3])
        else:
            self.gameStart(conf.beginLevel, conf.lives)
        self.resultsStart()
        self.sessionTimer.reset()

    def resultsStart(self):
        self.gameResults = GameResults()

    def gameStart(self, level, lives):
        self.game = GameLogic(self.gameCount, level, lives)
        self.game.start()

    def update(self):
        if self.game.inGame:
            self.game.update()
        elif self.gameResults.inGame:
            self.gameResults.update()
        if self.gameResults.inGame and self.gameResults.isPaused() and conf.autoToNextLevel:
            self.startNewGame()
        if not self.game.inGame and not self.gameResults.inGame:
            # запуск после завершения игры, узнать результаты
            log.debug("передача результатов игры")
            conf.todayGamesData[self.gameCount] = self.game.sendGameResult()
            self.gameResults.bgColor = self.game.bgColor
            self.gameResults.getGameResult(self.gameCount)
            self.gameResults.inGame = True
        self.sessionTimer.update()
        self.lblTimer.setBgColor(self.game.bgColor)
        self.lblTimer.setText(self.sessionTimer.__str__())

    def draw(self, screen):
        if self.game.inGame:
            self.game.draw(screen)
        elif self.gameResults.inGame:
            self.gameResults.draw(screen)
        self.lblTimer.draw(screen)

    def keyUp(self):
        pass

    def keyDown(self):
        pass

    def keyPressed(self):
        if self.game.inGame:
            self.game.keyPressed()
        elif self.gameResults.inGame:
            if self.gameResults.keyPressed():  # запустить новую игру
                self.startNewGame()

    def startNewGame(self):
        self.gameResults.inGame = False
        self.calculateNextLevel()
        self.gameCount += 1
        conf.todayGamesData[self.gameCount] = [
            self.gameResults.level, -1, -1, self.gameResults.lives, 0, 0]
        self.gameStart(self.gameResults.level, self.gameResults.lives)

    def calculateNextLevel(self):
        if self.gameResults.percent > conf.nextLevelPercent and not conf.manualMode:
            self.gameResults.level += 1
            self.gameResults.lives = conf.lives
        elif self.gameResults.percent < conf.dropLevelPercent and not conf.manualMode:
            self.gameResults.lives -= 1
            if self.gameResults.lives <= 0:
                self.gameResults.level -= 1
                self.gameResults.lives = conf.lives
            if self.gameResults.level < 1:
                self.gameResults.level = 1
                self.gameResults.lives = conf.lives
        log.debug("Вычислили новый уровень:%s жизней:%s",
                  self.gameResults.level, self.gameResults.lives)

    def quit(self):
        self.sessionTimer.pause()
        if self.gameResults.quit():
            self.app.sceneToday.getGames()
            self.app.setSceneToday()
        return False

    def resize(self):
        w, h = int(conf.w*0.2), int(conf.h*0.08)
        self.lblTimer.resize((conf.w/2-w/2, conf.h-h), (w, h))
        if self.game != None:
            self.game.resize()
            self.gameResults.resize()

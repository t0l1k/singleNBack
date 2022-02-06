import pygame
import conf
from scene import Scene
import today_games_data
import logging
import scene
from game_logic import GameLogic
from games_result import GameResults
from label import Label


log = logging.getLogger(__name__)


class SceneGame(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.sessionTimer = today_games_data.getTimer()
        self.setupTimerLabel()
        self.game = None

    def setupTimerLabel(self):
        w, h = int(conf.w*0.2), int(conf.h*0.08)
        self.lblTimer = Label("---", (conf.w/2-w/2, conf.h-h), (w, h))

    def entered(self):
        super().entered()
        if today_games_data.getSize() > 0:  # загрузить последний уровень и попытки
            last = today_games_data.getSize()-1
            self.gameStart(today_games_data.getLevelFromGame(last),
                           today_games_data.getLivesFromGame(last))
        else:
            self.gameStart(conf.beginLevel, conf.lives)
        self.resultsStart()
        self.sessionTimer.reset()
        if not conf.feedbackOnPreviousMove or conf.manualMode:
            self.lblTimer.visible = False

    def resultsStart(self):
        self.gameResults = GameResults()

    def gameStart(self, level, lives):
        self.game = GameLogic(today_games_data.getGameCount(), level, lives)
        self.game.start()

    def update(self, dt):
        self.sessionTimer.update()
        self.lblTimer.bg = self.game.bgColor
        self.lblTimer.text = self.sessionTimer.__str__()
        if not self.game.inGame and not self.gameResults.inGame:
            log.debug("После завершения игры, передать результаты")
            today_games_data.setDataDoneGame(self.game.sendGameResult())
            self.gameResults.setup(self.game.bgColor)
            if not conf.feedbackOnPreviousMove or conf.manualMode:
                self.lblTimer.visible = True
        if self.gameResults.inGame and self.gameResults.isPaused() and conf.autoToNextLevel:
            self.startNewGame()
        if self.game.inGame:
            self.game.update()
        elif self.gameResults.inGame:
            self.gameResults.update()
        self.lblTimer.update(dt)

    def draw(self, screen):
        if self.game.inGame:
            self.game.draw(screen)
        elif self.gameResults.inGame:
            self.gameResults.draw(screen)
        self.lblTimer.draw(screen)

    def key_up(self, key):
        super().key_up(key)
        if key == pygame.K_SPACE:
            if self.game.inGame:
                self.game.keyPressed()
            elif self.gameResults.inGame:
                if self.gameResults.keyPressed():
                    log.debug("запустить новую игру")
                    self.startNewGame()

    def startNewGame(self):
        self.gameResults.inGame = False
        if not conf.feedbackOnPreviousMove or conf.manualMode:
            self.lblTimer.visible = False
        level = today_games_data.getLevelFromGame(
            today_games_data.getGameCount())
        lives = today_games_data.getLivesFromGame(
            today_games_data.getGameCount())
        self.gameStart(level, lives)

    def quit(self):
        self.sessionTimer.pause()
        if self.gameResults.quit():
            today_games_data.saveGame()

    def resize(self):
        w, h = int(conf.w*0.2), int(conf.h*0.08)
        self.lblTimer.resize((conf.w/2-w/2, conf.h-h), (w, h))
        if self.game != None:
            self.game.resize()
            self.gameResults.resize()

import pygame
import conf
import window
from scene import Scene
import today_games_data
import logging
from game_logic import GameLogic
from game_result import GameResult
from label import Label
from gen_arr import Arr


log = logging.getLogger(__name__)


class SceneGame(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.sessionTimer = today_games_data.getTimer()
        self.lblTimer = Label("---", (0, 0), (1, 1))
        self.game = None
        self.resize()

    def entered(self):
        super().entered()
        self.resultsStart()
        self.sessionTimer.reset()
        if today_games_data.getSize() > 0:  # загрузить последний уровень и попытки
            self.startNewGame(True)
        else:
            self.gameStart(conf.defaultLevel,
                           conf.thresholdFallbackSessions, False)

    def resultsStart(self):
        self.gameResults = GameResult((0, 0), self.rect.size)

    def gameStart(self, level, lives, reset):
        if not reset:
            arr = Arr(level, GameLogic.getTotalMoves(level)).get()
        else:
            arr = today_games_data.getLastGameArr()
            level = today_games_data.getLastGameLevel()
            lives = today_games_data.getLastGameLives()
            print(arr, level, lives)
        self.game = GameLogic((0, 0), self.rect.size,
                              count=today_games_data.getGameCount(), level=level, lives=lives, arr=arr)
        self.game.start()

    def startNewGame(self, reset):
        self.gameResults.inGame = False
        level = today_games_data.getLevelFromGame(
            today_games_data.getGameCount())
        lives = today_games_data.getLivesFromGame(
            today_games_data.getGameCount())
        if reset:
            self.gameStart(level, lives, False)
        else:
            self.gameStart(level, lives, True)

    def update(self, dt):
        self.sessionTimer.update()
        if not self.game.inGame and not self.gameResults.inGame:
            log.debug("После завершения игры, передать результаты")
            today_games_data.setDataDoneGame(self.game.sendGameResult())
            self.gameResults.setup(self.game.bgColor)
        if self.gameResults.inGame and self.gameResults.isPaused() and conf.autoToNextLevel:
            self.startNewGame(True)
        if self.game.inGame:
            self.game.update(dt)
        elif self.gameResults.inGame:
            self.gameResults.update(dt)
            self.lblTimer.bg = self.game.bgColor
            self.lblTimer.text = self.sessionTimer.__str__()
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
                    self.startNewGame(True)
        elif key == pygame.K_RETURN:
            if self.gameResults.inGame:
                if self.gameResults.keyPressed():
                    log.debug("перезапустить последнюю игру")
                    self.startNewGame(False)
        elif key == pygame.K_F5:
            if self.game.inGame:
                conf.feedbackOnPreviousMove = not conf.feedbackOnPreviousMove
                if not conf.feedbackOnPreviousMove:
                    self.game.board.lblMove.visible = False
                else:
                    self.game.board.lblMove.visible = True
                log.debug("toogle feedback on previous move %s",
                          conf.feedbackOnPreviousMove)
        elif key == pygame.K_F1:
            if self.game.inGame:
                if conf.timeToNextCell < 5000:
                    conf.timeToNextCell += conf.incDurrationStep
                    conf.timeShowCell += conf.incDurrationStep
                    log.debug("time to next cell %s time show cell %s",
                              conf.timeToNextCell, conf.timeShowCell)
        elif key == pygame.K_F2:
            if self.game.inGame:
                if conf.timeToNextCell > conf.incDurrationStep*4:
                    conf.timeToNextCell -= conf.incDurrationStep
                    if conf.timeShowCell > 500:
                        conf.timeShowCell -= conf.incDurrationStep
                    log.debug("time to next cell %s time show cell %s",
                              conf.timeToNextCell, conf.timeShowCell)

    def quit(self):
        self.sessionTimer.pause()
        if self.gameResults.quit():
            today_games_data.saveGame()

    def resize(self):
        super().resize()
        w, h = int(window.rect.w*0.2), int(window.rect.h*0.08)
        self.lblTimer.resize(
            (window.rect.w/2-w/2, window.rect.h-h), (w, h))
        if self.game != None:
            ww = window.rect.w
            hh = window.rect.h
            pos, size = (0, 0), (ww, hh)
            self.gameResults.resize(pos, size)
            self.game.resize(pos, size)
            if not conf.feedbackOnPreviousMove or conf.manual:
                pos, size = (0, 0), (window.rect.w, window.rect.h)
                self.game.resize(pos, size)

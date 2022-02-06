import pygame
import sys
import conf
import scene
from scene_game import SceneGame
from scene_score import SceneScore
import today_games_data
from label import Label
import logging
from scene_today_results import ResultView

log = logging.getLogger(__name__)


class SceneToday(scene.Scene):
    name = "Scene Today"

    def __init__(self) -> None:
        super().__init__()
        self.setupScene()

    def setupScene(self):
        self.lblName = Label("Игры сегодня", (0, 0), (1, 1))
        self.lblTodayGames = Label("Игры за сегодня", (0, 0), (1, 1))
        self.resultsView = ResultView((0, 0), (100, 100))
        self.historyIndex = 0
        self.historyLenght = 0
        self.getStatistic()
        self.resize()

    def update(self, dt):
        super().update(dt)
        self.resultsView.update()
        self.lblName.update(dt)
        self.lblTodayGames.update(dt)

    def draw(self, screen):
        screen.fill(conf.bgColor)
        self.lblName.draw(screen)
        self.lblTodayGames.draw(screen)
        self.resultsView.draw(screen)

    def key_up(self, key):
        if key == pygame.K_ESCAPE:
            sys.exit()
        elif key == pygame.K_SPACE:
            if today_games_data.useHistory:
                today_games_data.loadData()
            scene.push(SceneGame())
        elif key == pygame.K_s:
            scene.push(SceneScore())
        elif key == pygame.K_LEFT:
            if self.historyLenght > self.historyIndex+1:
                self.historyIndex += 1
            if self.historyIndex >= 0:
                self.historyLenght = today_games_data.readHistory(
                    self.historyIndex)
            self.getStatistic()
            log.info("Выбрали дату назад %s", self.historyIndex)
        elif key == pygame.K_RIGHT:
            if self.historyIndex >= 0 and self.historyLenght > 0:
                self.historyIndex -= 1
            if self.historyIndex >= 0:
                self.historyLenght = today_games_data.readHistory(
                    self.historyIndex)
            else:
                today_games_data.loadData()
            self.getStatistic()
            log.info("Выбрали дату вперед %s", self.historyIndex)
        elif key == pygame.K_UP:
            log.info("Up pressed")
            self.resultsView.keyUp()
        elif key == pygame.K_DOWN:
            log.info("Down pressed")
            self.resultsView.keyDown()
        elif key == pygame.K_p:
            self.resultsView.plot = not self.resultsView.plot
            log.info("Сменили вид представления результатов за сегодня.")

    def resize(self):
        super().resize()
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

    def getStatistic(self):
        s = today_games_data.getTodayResults()
        log.debug(s)
        self.lblTodayGames.text = s
        for k, v in today_games_data.get():
            log.debug("#%s [%s]", k, v.__str__())
        self.resultsView.dirty = True

    def entered(self):
        super().entered()
        self.getStatistic()

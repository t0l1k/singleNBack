import pygame
import conf
from scene import Scene
import today_games_data
from label import Label
import logging
from scene_today_results import ResultView

log = logging.getLogger(__name__)


class SceneScore(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.lblName = Label("Результаты за весь период", (0, 0), (1, 1))
        self.resultsView = ResultView((0, 0), (100, 100), plot2=True)
        self.resize()

    def update(self, dt):
        self.resultsView.update()

    def draw(self, screen):
        screen.fill(conf.bgColor)
        self.lblName.draw(screen)
        self.resultsView.draw(screen)

    def key_up(self, key):
        super().key_up(key)
        if key == pygame.K_SPACE:
            if today_games_data.useHistory:
                today_games_data.loadData()
            self.app.setSceneGame()

    def resize(self):
        w, h = int(conf.w*0.3), int(conf.h*0.1)
        self.lblName.resize((0, 0), (w, h))
        w, h = conf.w*0.9, conf.h*0.85
        x, y = (conf.w-w)/2, conf.h-h*1.05
        self.resultsView.resize((x, y), (w, h))
        log.info("Scene Score resized")

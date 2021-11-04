import pygame
import conf
import today_games_data
from label import Label


class ResultView:
    def __init__(self, pos, size, boxHeight=20, rows=3) -> None:
        self.pos = pos
        self.image = pygame.Surface(size)
        self.boxHeight = boxHeight
        self.rows = rows
        self.rect = self.image.get_rect()
        self.createImage()

    def createImage(self):
        self.board = pygame.Surface(
            (self.rect.w, getHeihtForSurface(self.rect.h, self.rows)[0]))
        self.board_rect = self.board.get_rect()
        self.board.fill(conf.cellActiveColor)
        boxWidth = self.rect.w//self.rows
        boxHeight = getHeihtForSurface(self.rect.h, self.rows)[1]
        s = today_games_data.getDoneLevelsStr()
        for idx, _ in enumerate(s):
            x = idx % self.rows
            y = idx//self.rows
            l = Label(s[idx], (x*boxWidth, y*boxHeight),
                      (boxWidth, boxHeight))
            if today_games_data.getPercentFromGame(idx) > conf.nextLevelPercent:
                l.setBgColor(conf.regularColor)
            elif today_games_data.getPercentFromGame(idx) < conf.dropLevelPercent and today_games_data.useExtraTry(idx):
                l.setBgColor(conf.warningColor)
            elif today_games_data.getPercentFromGame(idx) < conf.dropLevelPercent and not today_games_data.useExtraTry(idx):
                l.setBgColor(conf.errorColor)
            else:
                l.setBgColor(conf.correctColor)
            l.draw(self.board)
        self.rect.clamp_ip(self.board_rect)
        self.image = self.board.subsurface(self.rect)
        self.dirty = False

    def keyUp(self):
        self.rect.y += -10
        self.dirty = True

    def keyDown(self):
        self.rect.y -= -10
        self.dirty = True

    def update(self):
        if self.dirty:
            self.createImage()

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def resize(self, pos, size):
        self.pos = pos
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.createImage()


def getHeihtForSurface(hH, rows):
    lenght = today_games_data.getLastDoneGame(
    ) if today_games_data.getLastDoneGame()/rows > 0 else 1
    size = conf.w*0.05
    boxHeight = size
    hSurf = boxHeight*lenght
    if boxHeight*lenght < hH:
        boxHeight = hH/lenght
        hSurf = boxHeight*lenght
        if boxHeight < size:
            boxHeight = size
            hSurf = boxHeight*lenght
        elif boxHeight > size:
            boxHeight = size
            hSurf = hH
    return (hSurf, boxHeight)

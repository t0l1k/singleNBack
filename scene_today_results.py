import pygame
import conf
from label import Label


class ResultView:
    def __init__(self, pos, size, boxHeight=50, rows=3) -> None:
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
        boxWidth = self.rect.w/self.rows
        boxHeight = getHeihtForSurface(self.rect.h, self.rows)[1]
        keys = list(conf.todayGamesData.keys())
        values = list(conf.todayGamesData.values())
        for y in range(len(conf.todayGamesData)//self.rows):
            for x in range(self.rows):
                idx = y*self.rows+x
                s = "#{} Уровень:{} Процент:{}".format(
                    keys[idx], values[idx][0], values[idx][5])
                l = Label(s, (x*boxWidth, y*boxHeight),
                          (boxWidth, boxHeight))
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
    lenght = len(conf.todayGamesData) if len(
        conf.todayGamesData)/rows > 0 else 1
    size = conf.w*0.06
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

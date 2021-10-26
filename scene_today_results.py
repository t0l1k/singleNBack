import pygame
import conf
from label import Label


class ResultView:
    def __init__(self, pos, size, boxHeight=50) -> None:
        self.pos = pos
        self.image = pygame.Surface(size)
        self.boxHeight = boxHeight
        self.rect = self.image.get_rect()
        self.createImage()

    def createImage(self):
        self.board = pygame.Surface(
            (self.rect.w, getHeihtForSurface(self.rect.h)[0]))
        self.board_rect = self.board.get_rect()
        self.board.fill((0, 128, 128))
        boxWidth = self.rect.w/2
        boxHeight = getHeihtForSurface(self.rect.h)[1]
        keys = list(conf.todayGamesData.keys())
        values = list(conf.todayGamesData.values())
        for y in range(len(conf.todayGamesData)//2):
            for x in range(2):
                idx = y*2+x
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


def getHeihtForSurface(hH):
    lenght = len(conf.todayGamesData) if len(conf.todayGamesData)/2 > 0 else 1
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

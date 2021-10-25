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
        i = 0
        boxHeight = getHeihtForSurface(self.rect.h)[1]
        for k, v in conf.todayGamesData.items():
            s = "#{} Уровень:{} Процент:{} Правильных:{} Ошибок:{}".format(
                k, v[0], v[5], v[1], v[2])
            l = Label(s, (0, i*boxHeight), (self.rect.w, boxHeight))
            l.draw(self.board)
            i += 1
            print(s)
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
    lenght = len(conf.todayGamesData) if len(conf.todayGamesData) > 0 else 1
    boxHeight = 50
    hSurf = boxHeight*lenght
    if boxHeight*lenght < hH:
        boxHeight = hH/lenght
        hSurf = boxHeight*lenght
        if boxHeight < 50:
            boxHeight = 50
            hSurf = boxHeight*lenght
        elif boxHeight > 50:
            boxHeight = 50
            hSurf = hH
    return (hSurf, boxHeight)

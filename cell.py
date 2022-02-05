import pygame
import conf
from drawable import Drawable


class Cell(Drawable):
    def __init__(self, pos, size, isCenter, bg=conf.bgColor, fg=conf.fgColor):
        super().__init__(pos, size, bg, fg)
        self.isCenter = isCenter
        self.margin = int(size[0]*0.12)
        self._bg = conf.cellBgColor
        self._active = False

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self._dirty = True

    def layout(self):
        if self.active:
            image = self.layoutActive()
        else:
            image = self.layoutDefault()
        return image

    def layoutDefault(self):
        image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        rect = pygame.Rect((0, 0), self.rect.size)
        pygame.draw.rect(image, self._bg, rect, border_radius=8)
        pygame.draw.rect(image, conf.cellFgColor, rect, 3, border_radius=8)
        self.setDot(image)
        return image

    def layoutActive(self):
        image = pygame.Surface((self.rect.w, self.rect.h))
        image.fill(self._bg)
        rect = pygame.Rect((0, 0), self.rect.size)
        pygame.draw.rect(image, conf.cellFgColor, rect, 3, border_radius=8)
        pygame.draw.rect(image, conf.cellActiveColor, (self.margin, self.margin,
                         rect.w-self.margin*2, rect.h-self.margin*2), border_radius=8)
        self.setDot(image)
        return image

    def setDot(self, image):
        if self.isCenter:
            margin = self.rect.h*0.45
            x1 = self.rect.w/2
            y1 = margin
            x2 = self.rect.w/2
            y2 = self.rect.h - margin
            pygame.draw.line(image, conf.cellFgColor, (x1, y1), (x2, y2))
            x1 = margin
            y1 = self.rect.h/2
            x2 = self.rect.w-margin
            y2 = self.rect.h/2
            pygame.draw.line(image, conf.cellFgColor, (x1, y1), (x2, y2))

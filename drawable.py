import pygame
import conf


class Drawable:
    def __init__(self, pos, size, bg=conf.bgColor, fg=conf.fgColor):
        self.rect = pygame.rect.Rect(pos, size)
        self._bg = bg
        self._fg = fg
        self._visible = True
        self._dirty = True
        self.image = None

    @property
    def bg(self):
        return self._bg

    @bg.setter
    def bg(self, value):
        if self._bg == value:
            return
        if self.visible:
            self._bg = value
            self.image = self.layout()

    @property
    def fg(self):
        return self._fg

    @fg.setter
    def fg(self, value):
        if self._fg == value:
            return
        if self.visible:
            self._fg = value
            self.image = self.layout()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        if value:
            self.image = self.layout()

    def layout(self):
        return pygame.Surface(self.rect.size)

    def update(self, dt):
        if self._dirty:
            self.image = self.layout()
            self._dirty = False

    def draw(self, surface):
        if self._visible:
            surface.blit(self.image, self.rect)

    def resize(self, pos, size):
        rect = pygame.Rect(pos, size)
        if self.rect == rect:
            return
        if self._visible:
            self.rect = rect
            self.image = self.layout()

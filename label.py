import pygame
import conf
from drawable import Drawable


class Label(Drawable):
    def __init__(self, text, pos, size, bg=conf.bgColor, fg=conf.fgColor, drawRect=True):
        super().__init__(pos, size, bg, fg)
        self._text = text
        self.drawRect = drawRect

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text == value:
            return
        if self.visible:
            self._text = value
            self._dirty = True

    def layout(self):
        image = super().layout()
        rect = pygame.Rect((0, 0), (self.rect.size))
        if self.drawRect:
            pygame.draw.rect(image, self.bg, rect, border_radius=8)
            pygame.draw.rect(image, self.fg, rect, 1, border_radius=8)
        font = pygame.font.SysFont(None, self.getFontSize())
        text = font.render(self._text, True, self._fg)
        x = self.rect.w/2-text.get_width()//2
        y = self.rect.h/2-text.get_height()//2
        image.blit(text, (x, y))
        return image

    def getFontSize(self):
        # подограть размер шрифта, чтобы поместилать вся строчка
        percent = 0.75
        size = self.rect.h if self.rect.w > self.rect.h else self.rect.w
        font_size = int(size*percent)
        if size == 1:
            # Есть уловка при первом создании экземпляра, даються размеры 1,1 пиксель
            return font_size
        font = pygame.font.SysFont(None, font_size)
        while (self.rect.width < font.size(self._text)[0]):
            font_size = int(size*percent)
            font = pygame.font.SysFont(None, font_size)
            percent -= 0.05
        return font_size

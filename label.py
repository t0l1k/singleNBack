import pygame
import conf


class Label:
    def __init__(self, str, pos, size, bg=conf.bgColor, fg=conf.fgColor) -> None:
        self.str = str
        self.pos = pos
        self.bg = bg
        self.fg = fg
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])
        self.image = self.setImage()
        self.visible = True

    def setImage(self):
        image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        pygame.draw.rect(image, self.bg, self.rect, border_radius=8)
        pygame.draw.rect(image, self.fg, self.rect, 3, border_radius=8)
        size = self.rect.h if self.rect.w > self.rect.h else self.rect.w
        font = pygame.font.SysFont(None, int(size*0.4))
        text = font.render(self.str, True, self.fg)
        x = self.rect.w/2-text.get_width()//2
        y = self.rect.h/2-text.get_height()//2
        image.blit(text, (x, y))
        return image

    def setText(self, str):
        if self.visible:
            self.str = str
            self.image = self.setImage()

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.pos)

    def setBgColor(self, color):
        if self.visible:
            self.bg = color
            self.image = self.setImage()

    def setPos(self, pos):
        if self.visible:
            self.pos = pos

    def setSize(self, size):
        if self.visible:
            self.rect = pygame.rect.Rect(0, 0, size[0], size[1])
            self.image = self.setImage()

    def resize(self, pos, size):
        if self.visible:
            self.setPos(pos)
            self.setSize(size)

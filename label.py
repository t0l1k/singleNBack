import pygame
import conf


class Label:
    def __init__(self, str, pos, size, bg=conf.black, fg=conf.aqua) -> None:
        self.str = str
        self.pos = pos
        self.bg = bg
        self.fg = fg
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])
        self.image = self.setImage()
        self.visible = True

    def setImage(self):
        image = pygame.Surface((self.rect.w, self.rect.h))
        image.fill(self.bg)
        pygame.draw.rect(image, self.fg, self.rect, 3)
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

    def setPos(self, pos):
        self.pos = pos

    def setSize(self, size):
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])
        self.image = self.setImage()

    def resize(self, pos, size):
        self.setPos(pos)
        self.setSize(size)

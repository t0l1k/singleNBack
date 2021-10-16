import pygame
import conf


class Label:
    def __init__(self, str, pos, size) -> None:
        self.str = str
        self.pos = pos
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])
        self.image = self.setImage()
        self.visible = True

    def setImage(self):
        image = pygame.Surface((self.rect.w, self.rect.h))
        image.fill(conf.cellBgColor)
        pygame.draw.rect(image, conf.cellFgColor, self.rect, 3)
        font = pygame.font.SysFont(None, int(self.rect.h*0.7))
        text = font.render(self.str, True, conf.cellFgColor)
        x = self.rect.w/2-text.get_width()//2
        y = self.rect.h/2-text.get_height()//2
        image.blit(text, (x, y))
        return image

    def setText(self, str):
        self.str = str
        self.image = self.setImage()

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.pos)

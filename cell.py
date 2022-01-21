import pygame
import conf


class Cell:
    def __init__(self, pos, size) -> None:
        self.pos = pos
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.margin = int(size*0.12)
        self.bg = conf.cellBgColor
        self.image = self.setImage()
        self.imageActive = self.setImageActive()
        self.active = False

    def setImage(self):
        image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        pygame.draw.rect(image, self.bg, self.rect, border_radius=8)
        pygame.draw.rect(image, conf.cellFgColor,
                         self.rect, 3, border_radius=8)
        return image

    def setImageActive(self):
        image = pygame.Surface((self.rect.w, self.rect.h))
        image.fill(self.bg)
        pygame.draw.rect(image, conf.cellFgColor,
                         self.rect, 3, border_radius=8)
        pygame.draw.rect(image, conf.cellActiveColor,
                         (self.margin, self.margin, self.rect.w-self.margin*2, self.rect.h-self.margin*2), border_radius=8)
        return image

    def draw(self, screen):
        if self.active:
            screen.blit(self.imageActive, self.pos)
        else:
            screen.blit(self.image, self.pos)

    def setBg(self, color):
        self.bg = color
        self.image = self.setImage()
        self.imageActive = self.setImageActive()

    def setPos(self, pos):
        self.pos = pos

    def setSize(self, size):
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.margin = int(size*0.12)

    def resize(self, pos, size):
        self.setPos(pos)
        self.setSize(size)
        self.image = self.setImage()
        self.imageActive = self.setImageActive()

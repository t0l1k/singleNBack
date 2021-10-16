import pygame
import conf


class Cell:
    def __init__(self, pos, size) -> None:
        self.pos = pos
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.margin = int(size*.05)
        self.active = False
        self.image = self.setImage()
        self.imageActive = self.setImageActive()

    def setImage(self):
        image = pygame.Surface((self.rect.w, self.rect.h))
        image.fill(conf.cellBgColor)
        pygame.draw.rect(image, conf.cellFgColor, self.rect, 3)
        return image

    def setImageActive(self):
        image = pygame.Surface((self.rect.w, self.rect.h))
        image.fill(conf.cellBgColor)
        pygame.draw.rect(image, conf.cellFgColor, self.rect, 3)
        pygame.draw.rect(image, conf.cellActiveColor,
                         (self.margin, self.margin, self.rect.w-self.margin*2, self.rect.h-self.margin*2))
        return image

    def draw(self, screen):
        if self.active:
            screen.blit(self.imageActive, self.pos)
        else:
            screen.blit(self.image, self.pos)

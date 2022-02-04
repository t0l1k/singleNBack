import pygame
import conf


class Cell:
    def __init__(self, pos, size, isCenter) -> None:
        self.pos = pos
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.isCenter = isCenter
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
        self.setDot(image)
        return image

    def setImageActive(self):
        image = pygame.Surface((self.rect.w, self.rect.h))
        image.fill(self.bg)
        pygame.draw.rect(image, conf.cellFgColor,
                         self.rect, 3, border_radius=8)
        pygame.draw.rect(image, conf.cellActiveColor,
                         (self.margin, self.margin, self.rect.w-self.margin*2, self.rect.h-self.margin*2), border_radius=8)
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

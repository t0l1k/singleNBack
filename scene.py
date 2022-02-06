import logging
from drawable import Drawable
import window
import pygame


stack = []
current = None


def push(sc):
    global current, stack
    stack.append(sc)
    current = sc
    current.entered()
    logging.info("Scene push %s %s", current, stack)


def pop():
    global current, stack
    if len(stack) > 0:
        current.quit()
        stack.pop()

    if len(stack) > 0:
        current = stack[len(stack)-1]
        current.entered()
    logging.info("Scene pop %s %s", current, stack)


class Scene(Drawable):
    name = "scene parent"

    def __init__(self) -> None:
        super().__init__(pos=window.rect.topleft, size=window.rect.size)

    def resize(self):
        self.pos = window.rect.topleft
        self.size = window.rect.size
        logging.info("Scene resize %s", self.name)

    def key_up(self, key):
        if key == pygame.K_ESCAPE:
            pop()
            logging.info("Request scene quit by escape key %s %s",
                         self.name, stack)

    def entered(self):
        logging.info("Entered scene %s", self.name)

    def quit(self):
        logging.info("Quit scene %s", self.name)

    def __str__(self) -> str:
        return "Scene: {}".format(self.name)

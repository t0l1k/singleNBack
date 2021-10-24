import pygame
import conf
from app import App
import logging as log


def main():
    pygame.init()
    pygame.display.set_caption("Single N Back")
    clock = pygame.time.Clock()
    fps = 30
    screen = setScreen(conf.isFullScreen)
    conf.w, conf.h = pygame.display.get_window_size()
    app = App()
    log.debug("init App")
    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
                log.debug("quit")
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_ESCAPE:
                    if app.quitScene():
                        done = True
                        log.debug("quit from app")
                elif e.key == pygame.K_SPACE:
                    app.keyPressed()
        app.update()
        app.draw(screen)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()


def setScreen(isFull):
    if isFull:
        screen = pygame.display.set_mode(
            (0, 0), pygame.NOFRAME)
        pygame.display.toggle_fullscreen()
    else:
        # w, h = pygame.display.list_modes()[7]
        w, h = 1024, 768
        screen = pygame.display.set_mode((w, h))
    return screen


if __name__ == "__main__":
    log.basicConfig(
        level=log.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[log.StreamHandler()])
    main()

import pygame
import conf
from app import App
import logging as log


def main():
    pygame.init()
    pygame.display.set_caption("Single N Back")
    clock = pygame.time.Clock()
    fps = 30
    screen = pygame.display.set_mode((conf.w, conf.h), pygame.RESIZABLE)
    conf.w, conf.h = pygame.display.get_window_size()
    app = App()
    log.debug("init App with screen size [%s %s]", conf.w, conf.h)
    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
                log.debug("quit")
            elif e.type == pygame.WINDOWRESIZED:
                w, h = pygame.display.get_window_size()
                mode = (640, 480)
                if w < mode[0]:
                    w = mode[0]
                if h < mode[1]:
                    h = mode[1]
                screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                conf.w, conf.h = pygame.display.get_window_size()
                app.resize()
                log.debug("App resized in width:%s height:%s", conf.w, conf.h)
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_ESCAPE:
                    if app.quitScene():
                        done = True
                        log.debug("quit from app")
                elif e.key == pygame.K_SPACE:
                    app.keyPressed()
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_UP]:
            app.keyUp()
        elif keyPressed[pygame.K_DOWN]:
            app.keyDown()
        app.update()
        app.draw(screen)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()


if __name__ == "__main__":
    log.basicConfig(
        level=log.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[log.StreamHandler()])
    main()

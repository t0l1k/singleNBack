import pygame
import today_games_data
import conf
from app import App
import logging 

log = logging.getLogger(__name__)


def main():
    pygame.init()
    pygame.display.set_caption("Single N Back")
    clock = pygame.time.Clock()
    fps = 30
    isFullScreen = False
    screen = setScreen(isFullScreen, (conf.w, conf.h))
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
                screen = setScreen(isFullScreen, (w, h))
                conf.w, conf.h = pygame.display.get_window_size()
                app.resize()
                log.debug("App resized in width:%s height:%s", conf.w, conf.h)
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_ESCAPE:
                    if app.quitScene():
                        done = True
                        log.debug("quit from app")
                elif e.key == pygame.K_F11:
                    isFullScreen = not isFullScreen
                    if isFullScreen:
                        size = (0, 0)
                    else:
                        size = (800, 600)
                    screen = setScreen(isFullScreen, size)
                    conf.w, conf.h = pygame.display.get_window_size()
                    app.resize()
                elif e.key == pygame.K_p:
                    app.sceneToday.resultsView.plot = not app.sceneToday.resultsView.plot
                    log.info("Сменили вид представления результатов за сегодня.")
                elif e.key == pygame.K_s:
                    app.keyS()
                elif e.key == pygame.K_LEFT:
                    app.keyTurnLeft()
                elif e.key == pygame.K_RIGHT:
                    app.keyTurnRight()
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


def setScreen(isFullScreen, size):
    flags = pygame.NOFRAME | pygame.FULLSCREEN if isFullScreen else pygame.RESIZABLE
    screen = pygame.display.set_mode(size, flags)
    conf.w, conf.h = pygame.display.get_window_size()
    log.debug("App in screen mode [%s, %s]", conf.w, conf.h)
    return screen


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()])
    today_games_data.loadData()
    main()

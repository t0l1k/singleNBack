import logging
import window
import scene
import pygame
import conf
import today_games_data

log = logging.getLogger(__name__)


def init(size=(800, 600), title="App", fullscreen=False):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()])
    today_games_data.loadData()
    log.debug("init app")
    pygame.init()
    window.surface = set_mode(fullscreen, size)
    pygame.display.set_caption(title)


def run():
    assert len(scene.stack) > 0
    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60)
        for e in pygame.event.get():
            running = handle_quit(e)
            handle_resize(e)
            handle_ui(e)
        scene.current.update(dt / 1000.0)
        scene.current.draw(window.surface)
        pygame.display.update()


def handle_ui(e):
    if e.type == pygame.KEYDOWN:
        scene.current.key_down(e.key)
    elif e.type == pygame.KEYUP:
        scene.current.key_up(e.key)


def handle_quit(e):
    if e.type == pygame.QUIT:
        log.debug("quit app")
        return False
    return True


def handle_resize(e):
    resized = False
    size = [800, 600]
    if e.type == pygame.WINDOWRESIZED:
        w, h = pygame.display.get_window_size()
        mode = (640, 480)
        if w < mode[0]:
            w = mode[0]
        if h < mode[1]:
            h = mode[1]
        size = [w, h]
        resized = True
    elif e.type == pygame.KEYUP:
        if e.key == pygame.K_F11:
            window.fullscreen = not window.fullscreen
            if window.fullscreen:
                size = (0, 0)
            else:
                size = (800, 600)
            resized = True
    if resized:
        window.surface = set_mode(window.fullscreen, size)
        conf.w, conf.h = pygame.display.get_window_size()
        if scene.current is not None:
            for sc in scene.stack:
                sc.resize()
                log.debug("scene %s resize", sc.name)
            logging.debug("Screen resized %s, %s",
                          window.rect, window.surface)


def set_mode(fullscreen, size):
    window.fullscreen = fullscreen
    size = (0, 0) if fullscreen else size
    flags = pygame.NOFRAME | pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
    screen = pygame.display.set_mode(size, flags)
    w, h = pygame.display.get_window_size()
    window.rect = pygame.Rect((0, 0), (w, h))
    logging.debug("App set screen mode [%s, %s]",
                  window.rect.width, window.rect.height)
    return screen


def quit():
    pygame.quit()

import pygame
import conf
from game_logic import GameLogic


def main():
    pygame.init()
    pygame.display.set_caption("Single N Back")
    clock = pygame.time.Clock()
    fps = 30
    screen = setScreen(conf.isFullScreen)
    conf.w, conf.h = pygame.display.get_window_size()
    done = False
    game = GameLogic()
    game.start()
    while not done:
        for e in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_ESCAPE] or e.type == pygame.QUIT:
                game.quit()
                done = True
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                game.keyPressed()
        game.update()
        game.draw(screen)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()


def setScreen(isFull):
    if isFull:
        screen = pygame.display.set_mode(
            (0, 0), pygame.NOFRAME)
        pygame.display.toggle_fullscreen()
    else:
        screen = pygame.display.set_mode((800, 600))
    return screen


if __name__ == "__main__":
    main()

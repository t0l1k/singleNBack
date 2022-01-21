import pygame
import logging 

log = logging.getLogger(__name__)
class Timer:
    def __init__(self) -> None:
        self.running = True
        self.paused = False
        self.startTime = 0
        if self.running:
            self.duration = 0
        log.info("Start timer")

    def reset(self):
        if self.paused:
            self.paused = False
        self.lastTick = self.getTick()
        log.info("Reset timer at %s", self.duration)

    def update(self):
        if self.running and not self.paused:
            self.startTime = self.getTick()
            self.duration += self.startTime-self.lastTick
            self.lastTick = self.startTime

    def stop(self):
        log.info("Stop timer")
        self.running = False
        self.paused = False

    def pause(self):
        self.paused = True
        log.info("Pause timer at %s", self.duration)

    def __str__(self) -> str:
        return "{:>02}:{:>02}".format(
            self.duration//1000//60, self.duration//1000 % 60)

    def getTick(self):
        return pygame.time.get_ticks()


instance = Timer()
log.info("Установили таймера новый экземпляр. %s", instance)

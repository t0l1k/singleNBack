import conf
import logging
import random
import time


log = logging.getLogger(__name__)


class Arr:
    def __init__(self, level, moves) -> None:
        self.level = level
        self.moves = moves

    def get(self):
        # Сгенерировать поле для игры, по настройкам
        # RR сколько процентов повторов
        # timeoutRR сколько времени на генерацию поля
        pause = conf.timeoutRR
        start = time.monotonic()
        count = 0
        check = False
        max = 0
        best = []
        while count < 100000 and time.monotonic()-start < pause and not check:
            arr = self.getNextArr()
            check, percent = self.checkRandomRepition(arr)
            if percent > max:
                max = percent
                best = arr
            count += 1
        if not check:
            log.info("Game selected with RR:%s", max)
            return best
        log.info("Game selected with RR:%s", percent)
        return arr

    def getNextArr(self):
        arr = []
        while(len(arr) < self.moves):
            number = random.randint(0, (conf.fieldSize*conf.fieldSize)-1)
            if (number != (conf.fieldSize*conf.fieldSize)//2 and not conf.useCenterCell) or conf.useCenterCell:
                arr.append(number)
        return arr

    def checkRandomRepition(self, arr):
        count = 0
        for i, v in enumerate(arr):
            nextMove = i+self.level
            if nextMove > len(arr)-1:
                break
            if v == arr[nextMove]:
                count += 1
        percent = int(100*count/len(arr))
        return percent > conf.RR and percent < 80, percent

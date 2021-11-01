import conf
import logging as log


def getMaxLevel():
    max = 0
    for k, v in get():
        level = v[0]
        if level > max and v[6]:
            max = level
    return max


def getAverage():
    sum = 0
    for k, v in get():
        if v[6]:
            sum += v[0]
    return round(sum/getLastDoneGame(), 2) if getLastDoneGame() > 0 else 0


def setDataDoneGame(data):
    # получить результаты завершенной игры и сделать новую запись для следующей игры
    add(data)
    level, lives = calculateNextLevel()
    setNewGameCount()
    newGame(level, lives)


def calculateNextLevel():
    percent = getPercentFromGame(getGameCount())
    level = getLevelFromGame(getGameCount())
    lives = getLivesFromGame(getGameCount())
    if percent > conf.nextLevelPercent and not conf.manualMode:
        level += 1
        lives = conf.lives
    elif percent < conf.dropLevelPercent and not conf.manualMode:
        lives -= 1
        if lives <= 0:
            level -= 1
            lives = conf.lives
        if level < 1:
            level = 1
            lives = conf.lives
    log.debug("Вычислили новый уровень:%s жизней:%s", level, lives)
    return (level, lives)


def add(data):
    __todayGamesData[getGameCount()] = data


def newGame(level, lives):
    """создать новую запись игры"""
    add([level, -1, -1, lives, 0, 0, False])


def get():
    """передать все данные"""
    return __todayGamesData.items()


def getKeys():
    """передать все ключи"""
    return list(__todayGamesData.keys())


def getValues():
    """передать всё содержимое ключей"""
    return list(__todayGamesData.values())


def getSize():
    """узнать размер массива"""
    return len(__todayGamesData)


def getGameCount():
    return __count


def setNewGameCount():
    global __count
    __count += 1


def getLevelFromGame(nr):
    """param nr: Узнать уровень по номеру игры"""
    return __todayGamesData[nr][0]


def getLivesFromGame(nr):
    """param nr: Узнать число попыток по номеру игры"""
    return __todayGamesData[nr][3]


def getPercentFromGame(nr):
    """param nr: Узнать процент по номеру игры"""
    return __todayGamesData[nr][5]


def getCountCorrectFromGame(nr):
    """param nr: Узнать сколько правильных ответов по номеру игры"""
    return __todayGamesData[nr][1]


def getCountWrongFromGame(nr):
    """param nr: Узнать сколько ошибочных ответов по номеру игры"""
    return __todayGamesData[nr][2]


def getLastDoneGame():
    """param nr: Узнать номер завершенной последней игры"""
    return __count if __count > 0 and __todayGamesData[__count][6] else __count - 1


def isDoneGame(nr):
    """param nr: Узнать завершена ли игра по номеру игры"""
    return __todayGamesData[nr][6]


def getDoneLevelsStr():
    arr = []
    for k, v in get():
        if v[6]:
            arr.append("#{} Level:{} Percent:{}".format(k, v[0], v[5]))
    return arr


def getDoneGamesStr():
    count = getSize()-1
    if not(isDoneGame(count)):
        count -= 1
    level = getLevelFromGame(count)
    percent = getPercentFromGame(count)
    correct = getCountCorrectFromGame(count)
    wrong = getCountWrongFromGame(count)
    return "#{} Уровень:{} процент:{} правильных:{} ошибок:{}".format(count, level, percent, correct, wrong)


#####
__count = 0
__todayGamesData = {}  # level, countCorrect, countWrong, lives, date, percent, done

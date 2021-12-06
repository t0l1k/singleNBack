import os
import pickle
import conf
import logging as log
from datetime import datetime
from gamedata import GameData
import scene_game_timer


def getTodayResults():
    return "{} Игр:{} Max:{} Avg:{} Игровое время:{}".format(
        getCurrentToday(),
        getLastDoneGame(),
        getMaxLevel(),
        getAverage(),
        countPlayTime())


def countPlayTime():
    t0 = 0  # всего миллисекунд
    for _, v in get():
        if v.isDone:
            t3 = 0  # дополнительное время при дополнительной попытке
            l = conf.lives - v.lives
            if l > 0:
                t3 = conf.incDurrationStep*l
            t1 = conf.timeToNextCell+t3
            t2 = conf.timeShowCell+t3
            t0 += t1 * v.moves + t2 / 2
    t0 = round(t0)
    s = "{:>02}:{:>02}.{:>03}".format(
        t0//1000//60, t0//1000 % 60, t0 % 1000)
    return s


def getDoneLevelsStr():
    arr = []
    for k, v in get():
        if v.isDone:
            arr.append("#{} Уровень:{} {}% Ходов:{} П:{} О:{}".format(
                k, v.level, v.percent, v.moves, v.countCorrect, v.countWrong))
    return arr


def parseGamesData():
    # данные для графика игр за сегодня
    x = []
    y = []
    color = []
    percent = []
    for k, v in get():
        if v.isDone:
            result = v.percent*0.01+v.level
            x.append(k)
            y.append(result)
            if getPercentFromGame(k) >= conf.nextLevelPercent:
                color.append("win")
            elif getPercentFromGame(k) < conf.dropLevelPercent and useExtraTry(k):
                color.append("extra try")
            elif getPercentFromGame(k) < conf.dropLevelPercent and not useExtraTry(k):
                color.append("lost")
            else:
                color.append("regular")
            percent.append(v.percent)
    return (x, y, color, percent)


def parseHistoryForPlot():
    # данные для графика результаты за весь период
    dt = []  # date results
    mx = []  # max results
    av = []  # average results
    try:
        with open(getHistoryPath(), 'r') as f:
            contents = f.readlines()
            if len(contents) < 2:
                raise FileNotFoundError
        for i, s in enumerate(contents):
            s = s.split()
            date = datetime.strptime(s[0], "%Y%m%d")
            max = s[2].split(":")[1]
            avg = s[3].split(":")[1]
            dt.append(date)
            mx.append(int(max))
            av.append(float(avg))
    except FileNotFoundError:
        return None, None, None
    return dt, mx, av


def getDoneGamesStr():
    count = getSize()-1
    if not(isDoneGame(count)):
        count -= 1
    level = getLevelFromGame(count)
    percent = getPercentFromGame(count)
    correct = getCountCorrectFromGame(count)
    wrong = getCountWrongFromGame(count)
    moves = getMoves(count)
    durration = getGameDurationStr(count)
    return "#{} Уровень:{} процент:{} правильных:{} ошибок:{} ходов:{} длительность:{}".format(count, level, percent, correct, wrong, moves, durration)


def getMaxLevel():
    max = 0
    for k, v in get():
        level = v.level
        if level > max and v.isDone:
            max = level
    return max


def getCurrentToday():
    if len(__todayGamesData) > 0:
        return __todayGamesData[0].dateBegin.strftime("%Y.%m.%d")
    return datetime.now().strftime("%Y%m%d")


def getAverage():
    sum = 0
    for k, v in get():
        if v.isDone:
            sum += v.level
    return round(sum/getLastDoneGame(), 2) if getLastDoneGame() > 0 else 0


def setDataDoneGame(data):
    # получить результаты завершенной игры и сделать новую запись для следующей игры
    if useHistory:
        loadData()
    add(data)
    level, lives, extraTry = calculateNextLevel()
    if extraTry:
        setExtraTry(getGameCount())
    setNewGameCount()
    newGame(level, lives)
    saveGame()


def calculateNextLevel():
    percent = getPercentFromGame(getGameCount())
    level = getLevelFromGame(getGameCount())
    lives = getLivesFromGame(getGameCount())
    extraTry = False
    if percent >= conf.nextLevelPercent and not conf.manualMode:
        level += 1
        lives = conf.lives
    elif percent < conf.dropLevelPercent and not conf.manualMode:
        lives -= 1
        extraTry = True
        if lives <= 0:
            level -= 1
            lives = conf.lives
            extraTry = False
        if level < 1:
            level = 1
            lives = conf.lives
    log.debug("Вычислили новый уровень:%s жизней:%s дополнительные попытки:%s",
              level, lives, extraTry)
    return (level, lives, extraTry)


def add(data: GameData):
    __todayGamesData[getGameCount()] = data


def newGame(level, lives):
    """создать новую запись игры"""
    defaultData = GameData(level, lives, 0, -1, -1, -1, False)
    add(defaultData)


def get():
    """передать все данные"""
    return __todayGamesData.items()


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
    return __todayGamesData[nr].level


def getLivesFromGame(nr):
    """param nr: Узнать число попыток по номеру игры"""
    return __todayGamesData[nr].lives


def getPercentFromGame(nr):
    """param nr: Узнать процент по номеру игры"""
    return __todayGamesData[nr].percent


def getCountCorrectFromGame(nr):
    """param nr: Узнать сколько правильных ответов по номеру игры"""
    return __todayGamesData[nr].countCorrect


def getCountWrongFromGame(nr):
    """param nr: Узнать сколько ошибочных ответов по номеру игры"""
    return __todayGamesData[nr].countWrong


def getMoves(nr):
    """param nr: Узнать сколько сделано ходов по номеру игры"""
    return __todayGamesData[nr].moves


def getLastDoneGame():
    """param nr: Узнать номер завершенной последней игры"""
    return __count if __count > 0 and __todayGamesData[__count].isDone else __count - 1


def isDoneGame(nr):
    """param nr: Узнать завершена ли игра по номеру игры"""
    return __todayGamesData[nr].isDone


def useExtraTry(nr):
    """param nr: Узнать использование дополнительной попытки по номеру игры"""
    return __todayGamesData[nr].useExtraTry


def setExtraTry(nr):
    """param nr: Установить использование дополнительной попытки по номеру игры"""
    __todayGamesData[nr].useExtraTry = True


def getGameDurationStr(nr):
    dt1 = __todayGamesData[nr].dateBegin
    dt2 = __todayGamesData[nr].dateEnd
    dur = dt2-dt1
    mSec = dur.microseconds
    seconds = dur.total_seconds()
    result = "{:02}:{:02}.{:03}".format(
        int(seconds//60), int(seconds % 60), int(mSec/1e3))  # minutes:seconds.milliseconds
    return result


def getTodayGamesPath():
    if not os.path.isdir("res"):
        os.makedirs("res")
    return os.path.join("res", "todayGames.pickle")


def getHistoryPath():
    return os.path.join("res", "history.txt")


def saveGame():
    if len(__todayGamesData) > 0:
        with open(getTodayGamesPath(), 'wb') as file:
            pickle.dump(__todayGamesData, file)
            pickle.dump(getTimer(), file)
        log.info("Сохранили новую запись последней игры.")


def saveHistory(day):
    s = "{} Игр:{} Max:{} Avg:{} Игровое время:{}".format(
        day,
        getLastDoneGame(),
        getMaxLevel(),
        getAverage(),
        countPlayTime())
    with open(getHistoryPath(), 'a') as file:
        if os.path.getsize(getHistoryPath()) > 0:
            file.write("\n"+s)
        else:
            file.write(s)
    os.rename(getTodayGamesPath(), os.path.join("res", day+'.pickle'))
    log.info("Сохранили результаты за %s в файл истории игр.", day)


def getHistoryGamesPath(day):
    return os.path.join("res", day+".pickle")


def readHistory(index):
    global useHistory
    contents = None
    try:
        with open(getHistoryPath(), 'r') as f:
            contents = f.readlines()
        idx = len(contents)-index-1
        if idx > len(contents):
            idx = len(contents)
        filename = contents[idx][:8]  # узнать дату
        filePath = getHistoryGamesPath(filename)
        with open(filePath, 'rb')as file:
            allData = pickle.load(file)
            timer = pickle.load(file)
            parseTodayGames(allData, timer)
    except FileNotFoundError:
        return 0
    useHistory = True
    return len(contents)


def loadData():
    todayStr = datetime.now().strftime("%Y%m%d")
    try:
        with open(getTodayGamesPath(), 'rb') as file:
            allData = pickle.load(file)
            timer = pickle.load(file)
            testDateStr = allData[0].dateBegin.strftime("%Y%m%d")
            if todayStr == testDateStr:
                log.info("Загрузили все данные игр за сегодня.")
                parseTodayGames(allData, timer)
            else:
                parseTodayGames(allData, timer)
                saveHistory(testDateStr)
                reset()
                log.info(
                    "Обнулить список игр за сегодня, сохранить вчерашние игры в историю.")
    except FileNotFoundError:
        reset()
        log.info("Первый запуск!")


def getTimer():
    return scene_game_timer.instance


def parseTodayGames(allData, timer):
    global __todayGamesData, __count
    __todayGamesData = allData
    __count = len(allData)-1
    scene_game_timer.instance == timer
    log.info("Восстановили игры за сегодня.")


def reset():
    global __todayGamesData, __count, __useHistory
    __count = 0
    __todayGamesData = {}
    __useHistory = False


@property
def useHistory():
    return __useHistory


@useHistory.setter
def useHistory(value):
    global __useHistory
    __useHistory = value


#####
__count = 0
__todayGamesData = {}  # GameData
__useHistory = False

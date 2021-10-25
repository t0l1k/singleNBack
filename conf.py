beginLevel = 1  # начальный уровень
manualMode = False  # играть только на одном уровне установленном в beginLevel
lives = 3  # число попыток
moves = 5  # базовое число ходов
maxMoves = 0  # ходов на уровне
nextLevelPercent = 80  # процент перехода при успехе
dropLevelPercent = 50  # процент перехода при поражении
resetLevelOnFirstWrong = True  # сбросить уровень при первой ошибке

timeToNextCell = 2000  # длительность до новой иконки
timeShowCell = 1000  # длительность показа иконки
timePause = 5  # желательная длина паузы между подходами
autoToNextLevel = False  # начать следующий уровень после истечения паузы

w, h = 0, 0
isFullScreen = False  # режим на весь экран
fieldSize = 3  # размер поля игры 2 и более, 3 классика

red = (255, 0, 0)  # цвет ошибки
green = (0, 255, 0)  # цвет правильного ответа
orange = (255, 165, 0)  # цвет ошибочного предположения
blue = (0, 0, 255)  # цвет отклика пользователя
gray = (192, 192, 192)
black = (0, 0, 0)
aqua = (0, 255, 255)
yellow = (255, 255, 0)

bgColor = gray  # цвет фона
cellBgColor = black  # цвет фона клетки
cellFgColor = aqua  # цвет текста клетки
cellActiveColor = yellow  # цвет активной клетки

#####
todayGamesData = {}  # level, countCorrect, countWrong, lives, date, percent
# todayGamesData = {0: [1, 0, 0,  0, 0, 100],
#                   1: [2, 0, 0,  0, 0, 100],
#                   2: [3, 0, 0,  0, 0, 100],
#                   3: [4, 0, 0,  0, 0, 0],
#                   4: [4, 0, 0,  0, 0, 66],
#                   5: [4, 0, 0,  0, 0, 100],
#                   6: [5, 0, 0,  0, 0, 50],
#                   7: [5, 0, 0,  0, 0, 50],
#                   8: [5, 0, 0,  0, 0, 0],
#                   9: [5, 0, 0,  0, 0, 50],
#                   10: [5, 0, 0, 0, 0, 50],
#                   11: [5, 0, 0, 0, 0, 0],
#                   12: [5, 0, 0, 0, 0, 0],
#                   13: [4, 0, 0, 1, 0, 50], }

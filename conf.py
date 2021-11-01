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
# увеличить продолжительность показа времени до новой клетки, если вопользовался дополнительной попыткой
incDurrationStep = 500
timePause = 5  # желательная длина паузы между подходами
autoToNextLevel = False  # начать следующий уровень после истечения паузы

w, h = 800, 600
fieldSize = 3  # ячеек на поле игры 2 и более, 3 классика

red = (255, 0, 0)  # цвет ошибки
green = (0, 255, 0)  # цвет правильного ответа
orange = (255, 165, 0)  # цвет ошибочного предположения
blue = (0, 0, 255)  # цвет отклика пользователя
gray = (144, 144, 144)
black = (0, 0, 0)
aqua = (0, 255, 255)
yellow = (255, 255, 0)
green1 = (178, 203, 50)
black1 = (41, 41, 41)
white1 = (252, 252, 252)

# theme 0
bgColor = gray
fgColor = white1
cellBgColor = bgColor
cellFgColor = fgColor
cellActiveColor = yellow
regularColor = blue
correctColor = green
errorColor = red
warningColor = orange

# # theme 1
# bgColor = black1
# fgColor = white1
# cellBgColor = bgColor
# cellFgColor = fgColor
# cellActiveColor = green1
# regularColor = blue
# correctColor = green1
# errorColor = red
# warningColor = orange

# theme 2
# bgColor = (49, 119, 108)
# fgColor = (253, 207, 127)
# regularColor = blue
# correctColor = green1
# errorColor = red
# warningColor = orange
# cellBgColor = bgColor
# cellFgColor = fgColor
# cellActiveColor = (178, 254, 250)

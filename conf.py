beginLevel = 1  # начальный уровень
manualMode = False  # играть только на одном уровне установленном в beginLevel
lives = 3  # число попыток
moves = 5  # базовое число ходов формула moves*level+level для 4го уровня это 5*4+4=24
nextLevelPercent = 80  # процент перехода при успехе
dropLevelPercent = 50  # процент перехода при поражении
resetLevelOnFirstWrong = False  # сбросить уровень при первой ошибке

timeToNextCell = 2000  # длительность до новой иконки
timeShowCell = 1000  # длительность показа иконки
incDurrationStep = 500  # увеличить продолжительность показа времени до новой клетки, если вопользовался дополнительной попыткой в миллисекундах
timePause = 5  # желательная длина паузы между подходами
autoToNextLevel = False  # начать следующий уровень после истечения паузы автоматически

RR = 30  # минимальный процент повтора random repition

fieldSize = 3  # ячеек на поле игры 2 и более, 3 классика

w, h = 800, 600  # размер окна при старте приложения


red = (255, 0, 0)
green = (0, 255, 0)
orange = (255, 165, 0)
blue = (0, 0, 255)
gray = (144, 144, 144)
black = (0, 0, 0)
aqua = (0, 255, 255)
yellow = (255, 255, 0)
green1 = (178, 203, 50)
black1 = (41, 41, 41)
white = (252, 252, 252)

# theme 0
bgColor = gray  # цвет фона окна
fgColor = white  # цвет текста в окне
cellBgColor = bgColor  # цвет фона поля ячейки
cellFgColor = fgColor  # цвет полос поля ячейки
cellActiveColor = yellow  # цвет показа ячейки
regularColor = blue  # цвет отклика пользователя
correctColor = green  # цвет правильного ответа
errorColor = red  # цвет пропуска отметить повтор
warningColor = orange  # цвет ошибочного предположения

# # theme 1
# bgColor = black1
# fgColor = white
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
# cellBgColor = bgColor
# cellFgColor = fgColor
# cellActiveColor = (178, 254, 250)
# regularColor = blue
# correctColor = green1
# errorColor = red
# warningColor = orange

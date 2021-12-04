beginLevel = 1  # начальный уровень
manualMode = False  # играть только на одном уровне установленном в beginLevel
lives = 3  # число попыток
moves = 6  # базовое число ходов формула moves*level для 4го уровня это 6*4=24
nextLevelPercent = 80  # процент перехода при успехе
dropLevelPercent = 50  # процент перехода при поражении
resetLevelOnFirstWrong = True  # сбросить уровень при первой ошибке

timeToNextCell = 2500  # длительность до новой иконки
timeShowCell = 1000  # длительность показа иконки
incDurrationStep = 500  # увеличить продолжительность показа времени до новой клетки, если вопользовался дополнительной попыткой в миллисекундах
timePause = 5  # желательная длина паузы между подходами
autoToNextLevel = False  # начать следующий уровень после истечения паузы автоматически

RR = 30  # минимальный процент повтора random repition
timeoutRR = 3  # сколько выделить секунд на генерацию RR

feedbackOnPreviousMove = True

fieldSize = 3  # ячеек на поле игры 2 и более, 3 классика

w, h = 800, 600  # размер окна при старте приложения

# theme orig
# bgColor = (128, 128, 128)  # цвет фона окна
# fgColor = (0, 0, 0)  # цвет текста
# cellBgColor = bgColor  # цвет фона поля ячейки
# cellFgColor = (0, 255, 255)  # цвет полос поля ячейки
# cellActiveColor = (255, 255, 0)  # цвет показа ячейки
# regularColor = (0, 0, 255)  # цвет отклика пользователя
# correctColor = (0, 255, 0)  # цвет правильного ответа
# errorColor = (255, 0, 0)  # цвет пропуска отметить повтор
# warningColor = (255, 165, 0)  # цвет ошибочного предположения

# theme monokai
bgColor = (46, 46, 46)
fgColor = (214, 214, 214)
cellBgColor = (46, 46, 46)
cellFgColor = (108, 153, 187)
cellActiveColor = (180, 210, 115)
regularColor = (108, 153, 187)
correctColor = (180, 210, 115)
errorColor = (176, 82, 121)
warningColor = (232, 125, 62)

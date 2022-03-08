import matplotlib
from matplotlib import ticker
import pylab
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pygame
import conf
import window
import today_games_data
from label import Label
import logging

log = logging.getLogger(__name__)


class ResultView:
    def __init__(self, pos, size, boxHeight=20,  plot=False, plot2=False, bg=conf.bgColor, fg=conf.fgColor):
        self.boxHeight = boxHeight
        self._rows = 1
        self._plot = plot
        self.plot2 = plot2
        self.resize(pos, size)

    def layout(self):
        if self.plot:
            image = self.layoutGraphTodayResults()
        elif self.plot2:
            data = today_games_data.parseHistoryForPlot()
            size = self.rect.h if self.rect.w > self.rect.h else self.rect.w
            dpi = size*100/300
            a, b = self.getAspectRatio()
            image = createPlot2(dpi, data, a, b)
        else:
            image = self.layoutLabels()
        return image

    def layoutGraphTodayResults(self):
        data = today_games_data.parseGamesData()
        xArr, yArr, colorsArr, percentsArr, levelsArr, movesPercent = data
        axisXMax = len(xArr)
        maxLevel = 0
        for level in levelsArr:
            if level > maxLevel:
                maxLevel = level
        maxLevel += 2
        axisYMax = maxLevel
        image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        bg = conf.bgColor
        fg = conf.fgColor
        image.fill(bg)
        margin = int(self.rect.w*0.05)
        axisRect = pygame.Rect(
            margin, margin, self.rect.width-margin*2, self.rect.height-margin*2)

        def lerp(t, inStart, inEnd, outStart, outEnd):
            return outStart + (t-inStart)/(inEnd-inStart)*(outEnd-outStart)

        def xPos(x):
            return round(lerp(x, 0, axisXMax, axisRect.left, axisRect.right))

        def yPos(y):
            return round(lerp(y, 0, axisYMax, axisRect.bottom, axisRect.top))
        # ось Х
        pygame.draw.line(image, fg, axisRect.bottomleft,
                         axisRect.bottomright, 3)
        xTicks = len(xArr)
        gridWidth = 0
        lastW = 0
        for i in range(1, xTicks+1):
            x = axisXMax*i/xTicks
            sizeBox = margin
            if i % 5 == 0 or i == 1 or i == xTicks:
                l = Label(str(int(x)),
                          (xPos(x)-sizeBox/2, axisRect.bottom+sizeBox*0.1),
                          (sizeBox, sizeBox), bg=bg, fg=fg, drawRect=False)
                l.draw(image)
            pygame.draw.line(
                image, fg,
                (xPos(x), axisRect.bottom),
                (xPos(x), axisRect.bottom+5), 3)
            pygame.draw.line(
                image, fg,
                (xPos(x), axisRect.bottom),
                (xPos(x), axisRect.top), 1)  # сетка
            gridWidth = xPos(x) - xPos(lastW)
            lastW = x
        if gridWidth > margin:
            gridWidth = margin
        # ось Y
        pygame.draw.line(image, fg, axisRect.bottomleft,
                         axisRect.topleft, 3)
        yTicks = maxLevel
        for i in range(1, yTicks+1):
            y = axisYMax*i/yTicks
            pygame.draw.line(
                image, fg,
                (axisRect.left, yPos(y)),
                (axisRect.left-5, yPos(y)), 3)
            pygame.draw.line(
                image, fg,
                (axisRect.left, yPos(y)),
                (axisRect.right, yPos(y)), 1)  # сетка
            sizeBox = int(axisRect.w*0.05)
            l = Label(str(i),
                      (axisRect.left-sizeBox*1.2, yPos(y)-sizeBox/2),
                      (sizeBox, sizeBox), bg=bg, fg=fg, drawRect=False)
            l.draw(image)
        sizeBox = margin
        l = Label("Уровень",
                  (axisRect.left-sizeBox, axisRect.top-sizeBox),
                  (sizeBox*2, sizeBox),  bg=bg, fg=fg, drawRect=False)
        l.draw(image)
        l = Label("Номер игры",
                  (axisRect.right-sizeBox*2, axisRect.bottom-sizeBox),
                  (sizeBox*2, sizeBox), bg=bg, fg=fg, drawRect=False)
        l.draw(image)
        sizeBox = margin*7
        l = Label("Результаты за день",
                  (axisRect.right/2-sizeBox/2+margin, axisRect.top-sizeBox/7),
                  (sizeBox, sizeBox/4), bg=bg, fg=fg, drawRect=False)
        l.draw(image)
        # данные
        points = []
        for x, y in zip(xArr, levelsArr):
            x += 1
            result = (xPos(axisXMax*x/len(xArr)), yPos(y))
            points.append(result)
        for p, q in zip(points, points[1:]):
            pygame.draw.line(image, conf.correctColor, p,
                             q, 3)  # уровень игры на старте
        points2 = []
        for x in xArr:
            x += 1
            result = (xPos(axisXMax*x/len(xArr)), yPos(0))
            points2.append(result)
        for p, q in zip(points, points2):
            pygame.draw.line(image, conf.errorColor, p, q, 3)
        points3 = []
        for x, percent in zip(xArr, movesPercent):
            x += 1
            result = (xPos(axisXMax*x/len(xArr)), yPos(percent))
            points3.append(result)
        for p, q in zip(points2, points3):
            pygame.draw.line(image, conf.regularColor, p, q, 5)
        points = []
        for x, y in zip(xArr, yArr):
            x += 1
            result = (xPos(axisXMax*x/len(xArr)), yPos(y))
            points.append(result)
        for p, q in zip(points, points[1:]):
            pygame.draw.line(image, conf.regularColor,
                             p, q, 2)  # результат игры
        values = []
        for percent in percentsArr:
            values.append(percent)
        for i, p in enumerate(points):
            col = "black"
            color = colorsArr[i]
            if color == "win":
                col = conf.regularColor
            elif color == "lost":
                col = conf.errorColor
            elif color == "regular":
                col = conf.correctColor
            elif color == "extra try":
                col = conf.warningColor
            sizeBox = gridWidth
            pygame.draw.circle(image, col, p, sizeBox/2)
            l = Label(str(values[i]),
                      (p[0]-sizeBox/2, p[1]-sizeBox/2),
                      (sizeBox, sizeBox), bg=bg, fg=fg, drawRect=False)
            l.draw(image)
        log.debug("today results graph plot done.")
        return image

    def layoutLabels(self):
        board = pygame.Surface(
            (self.rect.w, getLabelHeiht(self.rect.h, self.rows)[0]), pygame.SRCALPHA)
        board_rect = board.get_rect()
        pygame.draw.rect(board, conf.cellActiveColor,
                         self.rect, border_radius=8)
        boxWidth = self.rect.w//self.rows
        boxHeight = getLabelHeiht(self.rect.h, self.rows)[1]
        for k, v in today_games_data.get():
            idx = k
            if v.isDone:
                s = "#{} Уровень:{} {}% Ходов:{} П:{} О:{}".format(
                    k, v.level, v.percent, v.moves, v.countCorrect, v.countWrong)
                x = idx % self.rows
                y = idx//self.rows
                l = Label(s, (x*boxWidth, y*boxHeight),
                          (boxWidth, boxHeight), fg=conf.cellFgColor)
                if today_games_data.getPercentFromGame(idx) >= v.gamePreferences.nextLevelPercent:
                    l.bg = conf.regularColor
                elif today_games_data.getPercentFromGame(idx) < v.gamePreferences.dropLevelPercent and today_games_data.useExtraTry(idx):
                    l.bg = conf.warningColor
                elif today_games_data.getPercentFromGame(idx) < v.gamePreferences.dropLevelPercent and not today_games_data.useExtraTry(idx):
                    l.bg = conf.errorColor
                else:
                    l.bg = conf.correctColor
                l.draw(board)
        self.rect.clamp_ip(board_rect)
        image = board.subsurface(self.rect)
        return image

    def getAspectRatio(self):
        # узнать соотношение сторон
        w, h = self.rect.w, self.rect.h
        min = w if w < h else h
        max = w if w > h else h
        x = int(min/3)
        a = 1
        b = int(min/x)
        while (x*a < max):
            a += 1
        a -= 1
        return a, b

    def draw(self, surface):
        if self._dirty:
            self.image = self.layout()
            self._dirty = False
        surface.blit(self.image, self.pos)

    def resize(self, pos, size):
        self.pos = pos
        self.rect = pygame.Rect((0, 0), size)
        self._dirty = True

    @ property
    def rows(self):
        result = 3
        if window.rect.w <= 640:
            result = 1
        elif window.rect.w <= 800:
            result = 2
        elif window.rect.w <= 1024:
            result = 3
        else:
            result = 4
        return result

    @ rows.setter
    def rows(self, value):
        self._rows = value
        self._dirty = True

    @ property
    def plot(self):
        return self._plot

    @ plot.setter
    def plot(self, value):
        self._plot = value
        self._dirty = True


def getLabelHeiht(hH, rows):
    lenght = today_games_data.getLastDoneGame(
    ) if today_games_data.getLastDoneGame()/rows > 0 else 1
    size = hH*0.05
    boxHeight = size
    hSurf = boxHeight*lenght
    if boxHeight*lenght < hH:
        boxHeight = hH/lenght
        hSurf = boxHeight*lenght
        if boxHeight < size:
            boxHeight = size
            hSurf = boxHeight*lenght
        elif boxHeight > size:
            boxHeight = size
            hSurf = hH
    return (hSurf, boxHeight)


def createPlot2(dpi, data, w, h):
    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)
    matplotlib.use("Agg")
    plt.rcParams.update({
        "font.size": 5,
        "text.color": "white",
        "axes.facecolor": "grey",
        "axes.labelcolor": "green",
        "axes.edgecolor": "red",
        "axes.grid": "True",
        "grid.linestyle": ":",
        "xtick.color": "darkgrey",
        "ytick.color": "darkgrey",
        "grid.color": "darkgrey",
        "figure.facecolor": "grey",
        "figure.edgecolor": "grey",
    })
    fig = pylab.figure(figsize=[w, h], dpi=dpi)
    ax = fig.gca()
    ax.grid(True)
    x, yMax, yAvg = data
    if x is None or yMax is None or yAvg is None:
        return pygame.Surface((1, 1))
    ax.plot(x, yAvg, label="average", color="blue")
    ax.plot(x, yMax, label="max", color="red")
    ax.set_ylim(ymin=1)
    ax.legend()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    for i, date in enumerate(x):
        x1 = x[i]
        y1 = int(yMax[i])
        y2 = float(yAvg[i])
        plt.plot(x1, y1, "o", label="max", color="red")
        plt.plot(x1, y2, "o", label="average", color="blue")
    plt.grid(True)
    plt.show()
    fig.autofmt_xdate()
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    logger.setLevel(logging.DEBUG)
    return surf

import matplotlib
from matplotlib import ticker
import pylab
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pygame
import conf
import today_games_data
from label import Label


class ResultView:
    def __init__(self, pos, size, boxHeight=20,  plot=False, plot2=False) -> None:
        self.pos = pos
        self.image = pygame.Surface(size)
        self.boxHeight = boxHeight
        self._rows = 1
        self.rect = self.image.get_rect()
        self._plot = plot
        self.plot2 = plot2
        self.createImage()

    def createImage(self):
        if self.plot:
            data = today_games_data.parseGamesData()
            size = self.rect.h if self.rect.w > self.rect.h else self.rect.w
            dpi = size*100/300
            a, b = (4, 3) if self.rect.w > self.rect.h else (3, 3)
            self.image = createPlot(dpi, data, a, b)
        elif self.plot2:
            data = today_games_data.parseHistoryForPlot()
            size = self.rect.h if self.rect.w > self.rect.h else self.rect.w
            dpi = size*100/300
            a, b = (4, 3) if self.rect.w > self.rect.h else (3, 3)
            self.image = createPlot2(dpi, data, a, b)
        else:
            self.board = pygame.Surface(
                (self.rect.w, getLabelHeiht(self.rect.h, self.rows)[0]), pygame.SRCALPHA)
            self.board_rect = self.board.get_rect()
            pygame.draw.rect(self.board, conf.cellActiveColor,
                             self.rect, border_radius=8)
            boxWidth = self.rect.w//self.rows
            boxHeight = getLabelHeiht(self.rect.h, self.rows)[1]
            s = today_games_data.getDoneLevelsStr()
            for idx, _ in enumerate(s):
                x = idx % self.rows
                y = idx//self.rows
                l = Label(s[idx], (x*boxWidth, y*boxHeight),
                          (boxWidth, boxHeight))
                if today_games_data.getPercentFromGame(idx) >= conf.nextLevelPercent:
                    l.setBgColor(conf.regularColor)
                elif today_games_data.getPercentFromGame(idx) < conf.dropLevelPercent and today_games_data.useExtraTry(idx):
                    l.setBgColor(conf.warningColor)
                elif today_games_data.getPercentFromGame(idx) < conf.dropLevelPercent and not today_games_data.useExtraTry(idx):
                    l.setBgColor(conf.errorColor)
                else:
                    l.setBgColor(conf.correctColor)
                l.draw(self.board)
            self.rect.clamp_ip(self.board_rect)
            self.image = self.board.subsurface(self.rect)
        self.dirty = False

    def keyUp(self):
        self.rect.y += -self.boxHeight*2
        self.dirty = True

    def keyDown(self):
        self.rect.y -= -self.boxHeight*2
        self.dirty = True

    def update(self):
        if self.dirty:
            self.createImage()

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def resize(self, pos, size):
        self.pos = pos
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.createImage()

    @property
    def rows(self):
        result = 3
        if conf.w <= 640:
            result = 1
        elif conf.w <= 800:
            result = 2
        elif conf.w <= 1024:
            result = 3
        else:
            result = 4
        return result

    @rows.setter
    def rows(self, value):
        self._rows = value

    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, value):
        self._plot = value
        self.dirty = True


def getLabelHeiht(hH, rows):
    lenght = today_games_data.getLastDoneGame(
    ) if today_games_data.getLastDoneGame()/rows > 0 else 1
    size = hH*0.1
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


def createPlot(dpi, data, w, h):
    matplotlib.use("Agg")
    plt.rcParams.update({
        "lines.marker": "",
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
    fig.patch.set_alpha(0.1)
    ax = fig.gca()
    ax.grid(True)
    x, y, c, percent = data
    ax.plot(x, y)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    fig.autofmt_xdate()
    for i, color in enumerate(c):
        if color == "win":
            col = "blue"
            mark = "^"
        elif color == "lost":
            col = "red"
            mark = "v"
        elif color == "regular":
            col = "green"
            mark = "*"
        elif color == "extra try":
            col = "orange"
            mark = "."
        plt.plot(x[i], y[i], mark, color=col)
        plt.text(x[i], y[i], percent[i], ha='center',
                 va='center')
    plt.show()
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    return surf


def createPlot2(dpi, data, w, h):
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
    fig.patch.set_alpha(5)
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
    return surf

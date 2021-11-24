import matplotlib
import pylab
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pygame
import conf
import today_games_data
from label import Label


class ResultView:
    def __init__(self, pos, size, boxHeight=20, rows=3, plot=False) -> None:
        self.pos = pos
        self.image = pygame.Surface(size)
        self.boxHeight = boxHeight
        self.rows = rows
        self.rect = self.image.get_rect()
        self._plot = plot
        self.createImage()

    def createImage(self):
        if self.plot:
            data = today_games_data.parseGamesData()
            size = self.rect.h if self.rect.w > self.rect.h else self.rect.w
            dpi = size*100/300
            a, b = (4, 3) if self.rect.w > self.rect.h else (3, 3)
            self.image = createPlot(dpi, data, a, b)
        else:
            self.board = pygame.Surface(
                (self.rect.w, getHeihtForSurface(self.rect.h, self.rows)[0]), pygame.SRCALPHA)
            self.board_rect = self.board.get_rect()
            pygame.draw.rect(self.board, conf.cellActiveColor,
                             self.rect, border_radius=8)
            boxWidth = self.rect.w//self.rows
            boxHeight = getHeihtForSurface(self.rect.h, self.rows)[1]
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
        self.rect.y += -10
        self.dirty = True

    def keyDown(self):
        self.rect.y -= -10
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
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, value):
        self._plot = value
        self.dirty = True


def getHeihtForSurface(hH, rows):
    lenght = today_games_data.getLastDoneGame(
    ) if today_games_data.getLastDoneGame()/rows > 0 else 1
    size = conf.w*0.05
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

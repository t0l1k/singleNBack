from datetime import datetime


class GameData:
    dateBegin: datetime
    dateEnd: datetime

    def __init__(self, level=0, lives=0, moves=0, countCorrect=0, countWrong=0, percent=0, isDone=False, useExtraTry=False, dateBegin=0, dateEnd=0) -> None:
        self._dateBegin = dateBegin
        self._dateEnd = dateEnd
        self._level = level
        self._lives = lives
        self._moves = moves
        self._countCorrect = countCorrect
        self._countWrong = countWrong
        self._percent = percent
        self._isDone = isDone
        self._useExtraTry = useExtraTry

    @property
    def dateBegin(self):
        return self._dateBegin

    @dateBegin.setter
    def dateBegin(self, value):
        self._dateBegin = value

    @property
    def dateEnd(self):
        return self._dateEnd

    @dateEnd.setter
    def dateEnd(self, value):
        self._dateEnd = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value

    @property
    def moves(self):
        return self._moves

    @moves.setter
    def moves(self, value):
        self._moves = value

    @property
    def countCorrect(self):
        return self._countCorrect

    @countCorrect.setter
    def countCorrect(self, value):
        self._countCorrect = value

    @property
    def countWrong(self):
        return self._countWrong

    @countWrong.setter
    def countWrong(self, value):
        self._countWrong = value

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, value):
        self._percent = value

    @property
    def isDone(self):
        return self._isDone

    @isDone.setter
    def isDone(self, value):
        self._isDone = value

    @property
    def useExtraTry(self):
        return self._useExtraTry

    @useExtraTry.setter
    def useExtraTry(self, value):
        self._useExtraTry = value

    def __str__(self) -> str:
        return "Level:{} Lives:{} Moves:{} Correct:{} Wrong:{} Percent:{} Done:{} [{}] [{}]".format(self.level, self.lives, self.moves, self.countCorrect, self.countWrong, self.percent, self.isDone, self.dateBegin, self.dateEnd)

from datetime import datetime
import conf


class GameData:
    def __init__(self, level=0, lives=0, moves=-1, countCorrect=-1, countWrong=-1, percent=-1, isDone=False, useExtraTry=False, dateBegin=-1, dateEnd=-1, field=None) -> None:
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
        self._field = field
        self._gamePreferences = GamePreferences()

    @property
    def gamePreferences(self):
        result = None
        try:
            result = self._gamePreferences
        except AttributeError:
            self._gamePreferences = GamePreferences()
            result = self._gamePreferences
        return result

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value):
        self._field = value

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
        if type(self.dateBegin) == datetime:
            s = datetime.strftime(self.dateBegin, "%H:%M:%S.%f")[:-3]
        else:
            s = ""
        if type(self.dateEnd) == datetime:
            e = datetime.strftime(self.dateEnd, "%H:%M:%S.%f")[:-3]
        else:
            e = ""
        ss = ""
        try:
            ss = "Level:{} Lives:{} Moves:{} Correct:{} Wrong:{} Percent:{} [{}] [{}] {}".format(
                self.level, self.lives, self.moves, self.countCorrect, self.countWrong, self.percent, s, e, self.gamePreferences)
        except AttributeError:
            ss = "Level:{} Lives:{} Moves:{} Correct:{} Wrong:{} Percent:{} [{}] [{}]".format(
                self.level, self.lives, self.moves, self.countCorrect, self.countWrong, self.percent, s, e)
        finally:
            return ss


class GamePreferences:

    def __init__(self) -> None:
        self.manual = conf.manualMode
        self.toNextLevelGamesCount = conf.toNextLevelGamesCount
        self.nextLevelPercent = conf.nextLevelPercent
        self.dropLevelPercent = conf.dropLevelPercent
        self.resetLevelOnFirstWrong = conf.resetLevelOnFirstWrong
        self.fieldSize = conf.fieldSize

    def __str__(self) -> str:
        return "Settings[M:{},AM:{}Adv:{},Fb:{}RfE:{},Sz:{}]".format(self.manual, self.toNextLevelGamesCount, self.nextLevelPercent, self.dropLevelPercent, self.resetLevelOnFirstWrong, self.fieldSize)

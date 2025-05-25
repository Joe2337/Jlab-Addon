# coding: utf8
# Remark: When upgrading to Anki 2.1, the coding utf-8 and u'' unicode markers can be removed.
from aqt.qt import *
from Core.KanaTools import *

from Persistence.IStorable import *

MatrixIndex = collections.namedtuple("MatrixIndex", ["i", "j"])


class LearnedKana(QAbstractTableModel, IStorable):
    _numCols = 5
    _numRows = 11

    _aCol = 0
    _iCol = 1
    _uCol = 2
    _eCol = 3
    _oCol = 4

    _vovelRow = 0
    _kRow = 1
    _sRow = 2
    _tRow = 3
    _nRow = 4
    _hRow = 5
    _mRow = 6
    _yRow = 7
    _rRow = 8
    _wRow = 9
    _nRow = 10

    _nightMode = False

    # non-static members:
    # _characters: 2D-list with hiragana or katakana
    # _readings: 2D-list with readings for the characters
    # _valid: 2D-list indicating whether an index for a character is defined (not defined are e.g. yi or ye)
    # _learned: 2D-list indicating whether a character was learned

    def __init__(self):
        self.version = 0
        super(LearnedKana, self).__init__()
        self.init()

    def rowCount(self, parent):
        return self._numRows

    def columnCount(self, parent):
        return self._numCols

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role == Qt.ItemDataRole.DisplayRole:
            return self._characters[index.row()][index.column()] + " " + self._roumajiTooltips[index.row()][index.column()]
        elif role == Qt.ItemDataRole.ToolTipRole:
            return self._roumajiTooltips[index.row()][index.column()]
        elif role == Qt.ItemDataRole.BackgroundRole:
            if LearnedKana._nightMode:
                return QBrush(QColor(0, 200, 0)) if self._learned[index.row()][index.column()] else QBrush(QColor(150, 150, 150))
            else:
                return QBrush(Qt.GlobalColor.green) if self._learned[index.row()][index.column()] else QBrush(Qt.GlobalColor.white)
        return None

    def headerData(self, col, orientation, role):
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        elif self._valid[index.row()][index.column()]:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlag.ItemIsEnabled

    def initHiragana(self):
        self._characters = [
            ["あ", "い", "う", "え", "お"],
            ["か", "き", "く", "け", "こ"],
            ["さ", "し", "す", "せ", "そ"],
            ["た", "ち", "つ", "て", "と"],
            ["な", "に", "ぬ", "ね", "の"],
            ["は", "ひ", "ふ", "へ", "ほ"],
            ["ま", "み", "む", "め", "も"],
            ["や", "　", "ゆ", "　", "よ"],
            ["ら", "り", "る", "れ", "ろ"],
            ["わ", "　", "　", "　", "を"],
            ["　", "　", "　", "　", "ん"],
        ]

        self.initTooltips()
        self.initCharToIndexMap()
        self._identifier = "LearnedHiragana"

    def initKatakana(self):
        self._characters = [
            ["ア", "イ", "ウ", "エ", "オ"],
            ["カ", "キ", "ク", "ケ", "コ"],
            ["サ", "シ", "ス", "セ", "ソ"],
            ["タ", "チ", "ツ", "テ", "ト"],
            ["ナ", "ニ", "ヌ", "ネ", "ノ"],
            ["ハ", "ヒ", "フ", "ヘ", "ホ"],
            ["マ", "ミ", "ム", "メ", "モ"],
            ["ヤ", "　", "ユ", "　", "ヨ"],
            ["ラ", "リ", "ル", "レ", "ロ"],
            ["ワ", "　", "　", "　", "ヲ"],
            ["　", "　", "　", "　", "ン"],
        ]
        self.initTooltips()
        self.initCharToIndexMap()
        self._identifier = "LearnedKatakana"

    def initTooltips(self):
        self._roumajiTooltips = [
            ["a", "i", "u", "e", "o"],
            ["ka", "ki", "ku", "ke", "ko"],
            ["sa", "shi", "su", "se", "so"],
            ["ta", "chi", "tsu", "te", "to"],
            ["na", "ni", "nu", "ne", "no"],
            ["ha", "hi", "fu", "he", "ho"],
            ["ma", "mi", "mu", "me", "mo"],
            ["ya", "　", "yu", "　", "yo"],
            ["ra", "ri", "ru", "re", "ro"],
            ["wa", "　", "　", "　", "wo"],
            ["　", "　", "　", "　", "n"],
        ]

    def initCharToIndexMap(self):
        self._charToIndexMap = {}
        for i, row in enumerate(self._characters):
            for j, col in enumerate(row):
                self._charToIndexMap[col] = MatrixIndex(i, j)

    def toggleCharacter(self, index):
        if not index.isValid():
            return None
        if self._valid[index.row()][index.column()]:
            self._learned[index.row()][index.column()] = not self._learned[index.row()][index.column()]

    def getIndexForChar(self, char):
        result = self._charToIndexMap.get(char, 0)
        if result == 0:
            raise ValueError("Value not found")
        else:
            return result

    def setLearned(self, i, j):
        self._learned[i][j] = True

    def allLearned(self):
        for i, row in enumerate(self._learned):
            for j, col in enumerate(row):
                if self._valid[i][j] and not self._learned[i][j]:
                    return False
        return True

    def setAllLearned(self, val):
        for i, row in enumerate(self._learned):
            for j, col in enumerate(row):
                if self._valid[i][j]:
                    self._learned[i][j] = val
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    # there are some kana chars that are not shown in the kana table:
    # small ones, e.g.ゃ -> learned-state deduced from large counterpart: や
    # °"-ones, e.g. ぱ -> learned-state deduced from regular counterpart: は
    # this function maps them to their counterparts of the kana table. If no remapping is stored, the input is returned.
    # The function takes both hiragana and katakana chars as input, but the remapping is sotred as hiragana only.
    def remapChar(self, char):
        isKatakana = KanaTools.isKatakana(char)
        if isKatakana:
            char = KanaTools.kataToHira(char)

        remappedChar = self._hiraRemapping.get(char, 0)
        if remappedChar != 0:
            char = remappedChar

        if isKatakana:
            return KanaTools.hiraToKata(char)
        return char

    def isLearned(self, kanaInput):
        for curChar in kanaInput:
            try:
                matrixIndex = self.getIndexForChar(self.remapChar(curChar))
                if not self._learned[matrixIndex.i][matrixIndex.j]:
                    return False
            except ValueError:
                return False
        return True

    def toDictionary(self):
        return {"version": self.getVersion(), "identifier": self.getIdentifier(), "learned": self._learned}

    def fromDictionary(self, dictionary):
        version = dictionary["version"]
        self._learned = dictionary["learned"]

    def init(self):
        self._readings = [
            ["a", "i", "u", "e", "o"],
            ["ka", "ki", "ku", "ke", "ko"],
            ["sa", "shi", "su", "se", "so"],
            ["ta", "chi", "tsu", "te", "to"],
            ["na", "ni", "nu", "ne", "ne"],
            ["ha", "hi", "fu", "he", "ho"],
            ["ma", "mi", "mu", "me", "mo"],
            ["ya", "　", "yu", "　", "yo"],
            ["ra", "ri", "ru", "ru", "ro"],
            ["wa", "　", "　", "　", "wo"],
            ["　", "　", "　", "　", "n"],
        ]

        self._valid = [
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, False, True, False, True],
            [True, True, True, True, True],
            [True, False, False, False, True],
            [False, False, False, False, True],
        ]

        self._learned = [
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
        ]

        # This dictionary maps chars not displayed in the table to their counterparts that are displayed
        self._hiraRemapping = {
            "ぁ": "あ",
            "ぃ": "い",
            "ぅ": "う",
            "ぇ": "え",
            "ぉ": "お",
            "が": "か",
            "ゕ": "か",
            "ぎ": "き",
            "ぐ": "く",
            "げ": "け",
            "ご": "こ",
            "ざ": "さ",
            "じ": "し",
            "ず": "す",
            "ぜ": "せ",
            "ぞ": "そ",
            "だ": "た",
            "ぢ": "ち",
            "っ": "つ",
            "づ": "つ",
            "で": "て",
            "ど": "と",
            "ば": "は",
            "ぱ": "は",
            "び": "ひ",
            "ぴ": "ひ",
            "ぶ": "ふ",
            "ぷ": "ふ",
            "べ": "へ",
            "ぺ": "へ",
            "ぼ": "ほ",
            "ぽ": "ほ",
            "ゃ": "や",
            "ゅ": "ゆ",
            "ょ": "よ",
            "ゎ": "わ",
        }

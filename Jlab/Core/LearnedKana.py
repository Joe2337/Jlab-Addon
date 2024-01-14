#coding: utf8
#Remark: When upgrading to Anki 2.1, the coding utf-8 and u'' unicode markers can be removed.
from aqt.qt import *
from Core.KanaTools import *

from Persistence.IStorable import *

MatrixIndex = collections.namedtuple('MatrixIndex', ['i', u'j'])

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
            return self._characters[index.row()][index.column()] + u" " + self._roumajiTooltips[index.row()][index.column()]
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
        elif (self._valid[index.row()][index.column()]):
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlag.ItemIsEnabled

    def initHiragana(self):
        self._characters = [[u'あ', u'い', u'う', u'え', u'お'],
                            [u'か', u'き', u'く', u'け', u'こ'],
                            [u'さ', u'し', u'す', u'せ', u'そ'],
                            [u'た', u'ち', u'つ', u'て', u'と'],
                            [u'な', u'に', u'ぬ', u'ね', u'の'],
                            [u'は', u'ひ', u'ふ', u'へ', u'ほ'],
                            [u'ま', u'み', u'む', u'め', u'も'],
                            [u'や', u'　', u'ゆ', u'　', u'よ'],
                            [u'ら', u'り', u'る', u'れ', u'ろ'],
                            [u'わ', u'　', u'　', u'　', u'を'],
                            [u'　', u'　', u'　', u'　', u'ん']]

        self.initTooltips()
        self.initCharToIndexMap()
        self._identifier = u"LearnedHiragana"

    def initKatakana(self):
        self._characters = [[u'ア', u'イ', u'ウ', u'エ', u'オ'],
                            [u'カ', u'キ', u'ク', u'ケ', u'コ'],
                            [u'サ', u'シ', u'ス', u'セ', u'ソ'],
                            [u'タ', u'チ', u'ツ', u'テ', u'ト'],
                            [u'ナ', u'ニ', u'ヌ', u'ネ', u'ノ'],
                            [u'ハ', u'ヒ', u'フ', u'ヘ', u'ホ'],
                            [u'マ', u'ミ', u'ム', u'メ', u'モ'],
                            [u'ヤ', u'　', u'ユ', u'　', u'ヨ'],
                            [u'ラ', u'リ', u'ル', u'レ', u'ロ'],
                            [u'ワ', u'　', u'　', u'　', u'ヲ'],
                            [u'　', u'　', u'　', u'　', u'ン']]
        self.initTooltips()
        self.initCharToIndexMap()
        self._identifier = u"LearnedKatakana"

    def initTooltips(self):
        self._roumajiTooltips = [[u'a', u'i', u'u', u'e', u'o'],
                                 [u'ka', u'ki', u'ku', u'ke', u'ko'],
                                 [u'sa', u'shi', u'su', u'se', u'so'],
                                 [u'ta', u'chi', u'tsu', u'te', u'to'],
                                 [u'na', u'ni', u'nu', u'ne', u'no'],
                                 [u'ha', u'hi', u'fu', u'he', u'ho'],
                                 [u'ma', u'mi', u'mu', u'me', u'mo'],
                                 [u'ya', u'　', u'yu', u'　', u'yo'],
                                 [u'ra', u'ri', u'ru', u're', u'ro'],
                                 [u'wa', u'　', u'　', u'　', u'wo'],
                                 [u'　', u'　', u'　', u'　', u'n']]

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
            raise ValueError('Value not found')
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

    #there are some kana chars that are not shown in the kana table:
    #small ones, e.g.ゃ -> learned-state deduced from large counterpart: や
    #°"-ones, e.g. ぱ -> learned-state deduced from regular counterpart: は
    #this function maps them to their counterparts of the kana table. If no remapping is stored, the input is returned.
    #The function takes both hiragana and katakana chars as input, but the remapping is sotred as hiragana only.
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
        return {
            u"version" : self.getVersion(),
            u"identifier" : self.getIdentifier(),
            u"learned" : self._learned
        }

    def fromDictionary(self, dictionary):
        version = dictionary[u"version"]
        self._learned = dictionary[u"learned"]

    def init(self):
        self._readings = [[u'a', u'i', u'u', u'e', u'o'],
                          [u'ka', u'ki', u'ku', u'ke', u'ko'],
                          [u'sa', u'shi', u'su', u'se', u'so'],
                          [u'ta', u'chi', u'tsu', u'te', u'to'],
                          [u'na', u'ni', u'nu', u'ne', u'ne'],
                          [u'ha', u'hi', u'fu', u'he', u'ho'],
                          [u'ma', u'mi', u'mu', u'me', u'mo'],
                          [u'ya', u'　', u'yu', u'　', u'yo'],
                          [u'ra', u'ri', u'ru', u'ru', u'ro'],
                          [u'wa', u'　', u'　', u'　', u'wo'],
                          ['　', u'　', u'　', u'　', u'n']]

        self._valid = [[True, True, True, True, True],
                       [True, True, True, True, True],
                       [True, True, True, True, True],
                       [True, True, True, True, True],
                       [True, True, True, True, True],
                       [True, True, True, True, True],
                       [True, True, True, True, True],
                       [True, False, True, False, True],
                       [True, True, True, True, True],
                       [True, False, False, False, True],
                       [False, False, False, False, True]]

        self._learned = [[False, False, False, False, False],
                         [False, False, False, False, False],
                         [False, False, False, False, False],
                         [False, False, False, False, False],
                         [False, False, False, False, False],
                         [False, False, False, False, False],
                         [False, False, False, False, False],
                         [False, False, False, False, False],
                         [False, False, False, False, False],
                         [False, False, False, False, False],
                         [False, False, False, False, False]]

        #This dictionary maps chars not displayed in the table to their counterparts that are displayed
        self._hiraRemapping = {u'ぁ': u'あ',
                               u'ぃ': u'い',
                               u'ぅ': u'う',
                               u'ぇ': u'え',
                               u'ぉ': u'お',
                               u'が': u'か',
                               u'ゕ': u'か',
                               u'ぎ': u'き',
                               u'ぐ': u'く',
                               u'げ': u'け',
                               u'ご': u'こ',
                               u'ざ': u'さ',
                               u'じ': u'し',
                               u'ず': u'す',
                               u'ぜ': u'せ',
                               u'ぞ': u'そ',
                               u'だ': u'た',
                               u'ぢ': u'ち',
                               u'っ': u'つ',
                               u'づ': u'つ',
                               u'で': u'て',
                               u'ど': u'と',
                               u'ば': u'は',
                               u'ぱ': u'は',
                               u'び': u'ひ',
                               u'ぴ': u'ひ',
                               u'ぶ': u'ふ',
                               u'ぷ': u'ふ',
                               u'べ': u'へ',
                               u'ぺ': u'へ',
                               u'ぼ': u'ほ',
                               u'ぽ': u'ほ',
                               u'ゃ': u'や',
                               u'ゅ': u'ゆ',
                               u'ょ': u'よ',
                               u'ゎ': u'わ'}
from aqt.qt import *
from Core.KanaRoumajiTransliterator import *
from Core.ReadingAssistanceType import *

class DictTable(QTableWidget):
    expressionIndex = 0
    readingIndex = 1
    miscIndex = 2
    glossIndex = 3

    def __init__(self, parent):
        super(DictTable, self).__init__(parent)
        self.initUI()
        self._transliterator = None

    def setTransliterator(self, transliterator):
        assert isinstance(transliterator, KanaRoumajiTransliterator)
        self._transliterator = transliterator

    def initUI(self):
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(('Expression', 'Reading', 'Misc', 'Meaning'))
        #self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.setColumnWidth(self.expressionIndex, 150)
        self.setColumnWidth(self.readingIndex, 150)
        self.setColumnWidth(self.miscIndex, 150)
        self.horizontalHeader().setStretchLastSection(True)
        self.setWordWrap(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        #self.cellClicked.connect(self.cellClick)
        #self.doubleClicked.connect(self.cellDoubleClick)

    def addRow(self, expression, reading, misc, meaning):
        rowPosition = self.rowCount()
        self.insertRow(rowPosition)

        expressionItem = QTableWidgetItem(expression)
        expressionItem.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.setItem(rowPosition, self.expressionIndex, expressionItem)

        kanaItem = QTableWidgetItem(reading)
        kanaItem.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.setItem(rowPosition, self.readingIndex, kanaItem)

        miscItem = QTableWidgetItem(misc)
        miscItem.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.setItem(rowPosition, self.miscIndex, miscItem)

        meaningItem = QTableWidgetItem(meaning)
        meaningItem.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.setItem(rowPosition, self.glossIndex, meaningItem)

        self.resizeRowsToContents()

    def update(self, data, readingAssistanceType):
        if self._transliterator is None:
            raise Exception("KanaRoumajiTransliterator not set")

        while self.rowCount() != 0:
            self.removeRow(self.rowCount()-1)
        for row in data:
            readingDisplay = row[1]
            if readingAssistanceType == ReadingAssistanceType.latin:
                readingDisplay = self._transliterator.kanaToRoumaji(row[1], "", False, False)
            elif readingAssistanceType == ReadingAssistanceType.kanaTrainer:
                readingDisplay = self._transliterator.kanaToRoumaji(row[1], "", False, True)

            self.addRow(row[0], readingDisplay, row[2], row[4])

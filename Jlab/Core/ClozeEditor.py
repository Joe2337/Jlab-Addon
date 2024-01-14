from Core.ClozeEditorUi import *
from aqt.qt import *
from AnkiTools.JapaneseTextAccess import *
from Core.ReadingAssistanceType import *
from Core.KanaRoumajiTransliterator import *

class ClozeEditor(QDialog):

    def __init__(self, japaneseTextAccess, selectedText, learnedHiragana, learnedKatakana, transliterator, jDict, kanjium, readingAssistanceType):
        super(ClozeEditor, self).__init__()
        assert isinstance(transliterator, KanaRoumajiTransliterator)

        self._selectedText = selectedText
        self._learnedHiragana = learnedHiragana
        self._learnedKatakana = learnedKatakana
        self._transliterator = transliterator
        self._jDict = jDict

        self._japaneseTextAccess = japaneseTextAccess

        self._kanaQuery = u""
        self._kanjiQuery = u""
        self._lemmaQuery = u""
        self._initQueryPreselectionStrings(selectedText)

        self._ui = Ui_ClozeEditor()
        self._ui.setupUi(self)
        self._ui.searchTermLineEdit.setText(selectedText)
        self._ui.dictTableWidget.initUI() #this formats the table and overrides changes made by the auto-generated qt code
        self._ui.dictTableWidget.setTransliterator(transliterator)
        self._setFontSize(10)

        self._ui.lemmaRadioButton.clicked.connect(self.onLemmaRadioButtonClicked)
        self._ui.kanjiRadioButton.clicked.connect(self.onKanjiRadioButtonClicked)
        self._ui.kanaRadioButton.clicked.connect(self.onKanaRadioButtonClicked)
        self._ui.searchTermLineEdit.returnPressed.connect(self.searchEdited)
        self._ui.acceptButton.clicked.connect(self.onAcceptClicked)
        self._ui.dictTableWidget.cellClicked.connect(self._cellClicked)
        self._ui.dictTableWidget.doubleClicked.connect(self._cellDoubleClicked)
        self._ui.clozeTextLineEdit.returnPressed.connect(self.onAcceptClicked)
        self._ui.clozeSelectionLineEdit.installEventFilter(self)
        self._ui.clozeTextLineEdit.installEventFilter(self)
        self.installEventFilter(self)

        self._readingAssistanceType = readingAssistanceType

        self._ui.kanaDebugLineEdit.setText(self._japaneseTextAccess.getCleanedHiraganaCloze())
        self._ui.kanjiDebugLineEdit.setText(self._japaneseTextAccess.getCleanedKanjiCloze())

        self.initUiState()
        self.initConvenienceInputLabels()
        self.initClozeSelectionLineEdit()

        self._hiraganaClozePos = ClozePosition(0, 0)
        self._kanjiClozePos = ClozePosition(0, 0)
        self._hiraganaClozeResult = japaneseTextAccess.getOriginalHiraganaCloze()
        self._kanjiClozeResult = japaneseTextAccess.getOriginalKanjiCloze()
        self._searchResults = []
        self._lookedUpReadings = u""
        self._lookedUpExpression = u""

        #this will keep the selection in the debug views highlighed, together with the re-selection in the event filter
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#3a7fc2"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("white"))
        self._ui.kanaDebugLineEdit.setPalette(palette)
        self._ui.kanjiDebugLineEdit.setPalette(palette)

        QTimer.singleShot(1, lambda : self.search()) #without delayed search the table is not correctly formatted
        QTimer.singleShot(100, lambda: self.updateClozePositions(selectedText)) #without delay, the selection is not updated
        QTimer.singleShot(110, lambda: self._updateClozePreview())

    def _setFontSize(self, fontSize):
        f = self._ui.clozeSelectionLineEdit.font()
        f.setPointSize(fontSize)  # standard is 8
        self._ui.searchTermLineEdit.setFont(f)
        self._ui.clozeSelectionLineEdit.setFont(f)
        self._ui.kanaDebugLineEdit.setFont(f)
        self._ui.kanjiDebugLineEdit.setFont(f)
        self._ui.clozeTextLineEdit.setFont(f)
        self._ui.clozePreviewTextEdit.setFont(f)
        self._ui.kanjiLabel.setFont(f)
        self._ui.kanaLabel.setFont(f)
        self._ui.lemmaLabel.setFont(f)
        self._ui.clozePreviewTextEdit.setFixedHeight(self._ui.lemmaLabel.geometry().height() * 3)

    def _initQueryPreselectionStrings(self, selectedText):
        try:
            kanaKanjiLemma = self._japaneseTextAccess.getTextFragments(selectedText)
            self._kanaQuery = kanaKanjiLemma[0].replace(u" ", u"")
            self._kanjiQuery = kanaKanjiLemma[1].replace(u" ", u"")
            self._lemmaQuery = kanaKanjiLemma[2].replace(u" ", u"")
        except Exception:
            return

    def getHiraganaClozeResult(self):
        return self._hiraganaClozeResult

    def getKanjiClozeResult(self):
        return self._kanjiClozeResult

    def getLookedUpReadings(self):
        return self._lookedUpReadings

    def getLookedUpExpression(self):
        return self._lookedUpExpression

    def _cellClicked(self, row, col):
        self._processDictionarySelection(row)
        self._updateClozePreview()

    def _cellDoubleClicked(self, modelindex):
        self._processDictionarySelection(modelindex.row())
        self._finalize()

    def _manualClozeEdit(self):
        self._updateClozePreview()

    def _processDictionarySelection(self, row):
        miscModelIndex = self._ui.dictTableWidget.model().index(row, self._ui.dictTableWidget.miscIndex)
        miscItem = self._ui.dictTableWidget.itemFromIndex(miscModelIndex)

        glossModelIndex = self._ui.dictTableWidget.model().index(row, self._ui.dictTableWidget.glossIndex)
        glossItem = self._ui.dictTableWidget.itemFromIndex(glossModelIndex)

        self._lookedUpExpression = self._searchResults[row][self._ui.dictTableWidget.expressionIndex]
        self._lookedUpReadings = self._searchResults[row][self._ui.dictTableWidget.readingIndex]

        self._ui.clozeTextLineEdit.setText(TextFormatter.formatDictionaryInputForClozeSingleItem((miscItem.text(), glossItem.text()), 400))

    def _finalize(self):
        try:
            self._makeClozes()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        self.accept()

    def _makeClozes(self):
        if len(self._ui.clozeTextLineEdit.text()) == 0:
            raise Exception("No cloze hint defined")

        # note, that JapaneseTextAccess:getClozePositions already raises an exception, if either hiragana or kanji cloze
        # is not found. This exception is handled in ClozeEditor.updateClozePositions, where both cloze positions are
        # then set to (0, 0). This should probably be relaxed a bit, such that all found clozes are set. This requires
        # to remove the exceptions raised in JapaneseTextAccess, the cases then must be covered here.
        if self._hiraganaClozePos.length == 0 or self._kanjiClozePos.length == 0:
            raise Exception("Cloze position not found")

        clozeText = TextFormatter.wrapTextForCloze(self._ui.clozeTextLineEdit.text())
        self._hiraganaClozeResult = self._japaneseTextAccess.getNewHiraganaCloze(self._hiraganaClozePos, clozeText)
        self._kanjiClozeResult = self._japaneseTextAccess.getNewKanjiCloze(self._kanjiClozePos, clozeText)

    def eventFilter(self, object, event):
        if object is self._ui.clozeSelectionLineEdit and event.type() == QEvent.Type.MouseButtonRelease:
            self.updateClozeWithUserInput()
            return True
        if object is self._ui.clozeTextLineEdit and event.type() == QEvent.Type.KeyRelease:
            self._updateClozePreview()
            return True
        if object is self and event.type() == QEvent.Type.WindowActivate:
            self.selectClozePositionsInDebugView()
            return True
        return False

    def _updateClozePreview(self):
        try:
            self._makeClozes()
        except:
            return
        if self._readingAssistanceType == ReadingAssistanceType.latin:
            self._ui.clozePreviewTextEdit.setText(self._transliterator.kanaToRoumaji(self._hiraganaClozeResult, u"", False, False))
        elif self._readingAssistanceType == ReadingAssistanceType.kanaTrainer:
            self._ui.clozePreviewTextEdit.setText(self._transliterator.kanaToRoumaji(self._hiraganaClozeResult, u"", False, True))
        elif self._readingAssistanceType == ReadingAssistanceType.none:
            self._ui.clozePreviewTextEdit.setText(self._kanjiClozeResult)
        else:
            self._ui.clozePreviewTextEdit.setText("Not implemented for ReadingAssistanceType == " + self._readingAssistanceType)

    def updateClozeWithUserInput(self):
        if not self._ui.clozeSelectionLineEdit.hasSelectedText():
            return
        self.updateClozePositions(self._ui.clozeSelectionLineEdit.selectedText())
        self._updateClozePreview()

    def _getReadingAssistanceString(self, input):
        if len(input) == 0:
            return u""
        else:
            return u"  (" + input + u")"

        # if self._readingAssistanceType == ReadingAssistanceType._none:
        #     return u"  (" + input + u")"
        # if self._readingAssistanceType == ReadingAssistanceType._latin:
        #     return u"  (" + self._transliterator.kanaToRoumaji(input, u"", False, False) + u")"
        # elif self._readingAssistanceType == ReadingAssistanceType._kanaTrainer:
        #     return u"  (" + self._transliterator.kanaToRoumaji(input, u"", False, True) + u")"
        # else:
        #     raise ValueError(u"Not implemented for " + self._readingAssistanceType)

    def initConvenienceInputLabels(self):
        self._ui.kanaLabel.setText(self._getReadingAssistanceString(self._kanaQuery))
        self._ui.kanjiLabel.setText(self._getReadingAssistanceString(self._kanjiQuery))
        self._ui.lemmaLabel.setText(self._getReadingAssistanceString(self._lemmaQuery))

    def initClozeSelectionLineEdit(self):
        #this is rather for debugging purpose and could possibly be deleted later.
        if self._readingAssistanceType == ReadingAssistanceType.latin:
            self._ui.clozeSelectionLineEdit.setText(self._transliterator.kanaToRoumaji(self._japaneseTextAccess.getCleanedHiraganaCloze(), u"", False, False))
        elif self._readingAssistanceType == ReadingAssistanceType.kanaTrainer:
            self._ui.clozeSelectionLineEdit.setText(self._transliterator.kanaToRoumaji(self._japaneseTextAccess.getCleanedHiraganaCloze(), u"", False, True))
        elif self._readingAssistanceType == ReadingAssistanceType.none or self._readingAssistanceType == ReadingAssistanceType.kanjiTrainer:
            self._ui.clozeSelectionLineEdit.setText(self._japaneseTextAccess.getCleanedKanjiCloze())
        else:
            raise Exception("Not implemented")

    def updateClozePositions(self, selectedText):
        try:
            clozePos = self._japaneseTextAccess.getClozePositions(selectedText)
            self._hiraganaClozePos = clozePos[0]
            self._kanjiClozePos = clozePos[1]
            self.selectClozePositionsInDebugView()
            self._ui.infoLabel.setStyleSheet("color: green")
            self._ui.infoLabel.setText("New cloze positions found")
        except:
            self._hiraganaClozePos = ClozePosition(0, 0)
            self._kanjiClozePos = ClozePosition(0, 0)
            self._ui.infoLabel.setStyleSheet("color: red")
            self._ui.infoLabel.setText("Could not find new cloze positions")

    def selectClozePositionsInDebugView(self):
        if self._hiraganaClozePos.length != 0:
            self._ui.kanaDebugLineEdit.setSelection(self._hiraganaClozePos.start, self._hiraganaClozePos.length)
        if self._kanjiClozePos.length != 0:
            self._ui.kanjiDebugLineEdit.setSelection(self._kanjiClozePos.start, self._kanjiClozePos.length)

    def onAcceptClicked(self):
        self._finalize()

    def initUiState(self):
        kanaAvailable = len(self._kanaQuery) != 0
        kanjiAvailable = len(self._kanjiQuery) != 0
        lemmaAvailable = len(self._lemmaQuery) != 0

        self._ui.lemmaRadioButton.setEnabled(lemmaAvailable)
        self._ui.kanjiRadioButton.setEnabled(kanjiAvailable)
        self._ui.kanaRadioButton.setEnabled(kanaAvailable)

        if lemmaAvailable:
            self._ui.searchTermLineEdit.setText(self._lemmaQuery)
            self._ui.lemmaRadioButton.setChecked(True)

        if kanjiAvailable:
            if not lemmaAvailable:
                self._ui.searchTermLineEdit.setText(self._kanjiQuery)
                self._ui.kanjiRadioButton.setChecked(True)

        if kanaAvailable:
            if not lemmaAvailable and not kanjiAvailable:
                self._ui.searchTermLineEdit.setText(self._kanaQuery)
                self._ui.kanaRadioButton.setChecked(True)

    def searchEdited(self):
        #With Qt5, use QSignalBlocker
        self._ui.lemmaRadioButton.blockSignals(True)
        self._ui.kanjiRadioButton.blockSignals(True)
        self._ui.kanaRadioButton.blockSignals(True)

        self._ui.lemmaRadioButton.setAutoExclusive(False)
        self._ui.kanjiRadioButton.setAutoExclusive(False)
        self._ui.kanaRadioButton.setAutoExclusive(False)

        self._ui.lemmaRadioButton.setChecked(False)
        self._ui.kanjiRadioButton.setChecked(False)
        self._ui.kanaRadioButton.setChecked(False)

        self._ui.lemmaRadioButton.setAutoExclusive(True)
        self._ui.kanjiRadioButton.setAutoExclusive(True)
        self._ui.kanaRadioButton.setAutoExclusive(True)

        self.search()

        self._ui.lemmaRadioButton.blockSignals(False)
        self._ui.kanjiRadioButton.blockSignals(False)
        self._ui.kanaRadioButton.blockSignals(False)

    def search(self):
        self._searchResults = self._jDict.lookup(self._ui.searchTermLineEdit.text())
        self._ui.dictTableWidget.update(self._searchResults, self._readingAssistanceType)

    def enableQuickSelection(self, enable):
        self._ui.lemmaRadioButton.setEnabled(enable)
        self._ui.kanjiRadioButton.setEnabled(enable)
        self._ui.kanaRadioButton.setEnabled(enable)

    def onLemmaRadioButtonClicked(self):
        if self._ui.lemmaRadioButton.isEnabled():
            self._ui.searchTermLineEdit.setText(self._lemmaQuery)
            self.search()

    def onKanjiRadioButtonClicked(self):
        if self._ui.kanjiRadioButton.isEnabled():
            self._ui.searchTermLineEdit.setText(self._kanjiQuery)
            self.search()

    def onKanaRadioButtonClicked(self):
        if self._ui.kanaRadioButton.isEnabled():
            self._ui.searchTermLineEdit.setText(self._kanaQuery)
            self.search()






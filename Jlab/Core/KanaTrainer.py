from Persistence.IStorable import *
from Core.KanaTrainerUi import *
from Core.KanaTools import *
from Core.KanaTrainerData import *
from aqt.qt import *
import math

ordinal = lambda n: "%s" % ("tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

class KanaTrainer(QDialog, IStorable):

    def __init__(self, kanaTrainerData):
        assert isinstance(kanaTrainerData, KanaTrainerData)
        super(KanaTrainer, self).__init__()

        self._kanaTrainerData = kanaTrainerData

        self._ui = Ui_KanaTrainerDialog()
        self._ui.setupUi(self)
        self._ui.kanaTypeCombobox.addItem(KanaType.hiragana)
        self._ui.kanaTypeCombobox.addItem(KanaType.katakana)

        self._ui.hiraganaTableView.setModel(kanaTrainerData.learnedHiragana)
        self._ui.hiraganaTableView.resizeRowsToContents()
        self._ui.hiraganaTableView.resizeColumnsToContents()

        self._ui.katakanaTableView.setModel(kanaTrainerData.learnedKatakana)
        self._ui.katakanaTableView.resizeRowsToContents()
        self._ui.katakanaTableView.resizeColumnsToContents()

        self.resize((self._ui.hiraganaTableView.horizontalHeader().length() + 30)*2, self.height())

        self._ui.hiraganaTableView.doubleClicked.connect(kanaTrainerData.learnedHiragana.toggleCharacter)
        self._ui.katakanaTableView.doubleClicked.connect(kanaTrainerData.learnedKatakana.toggleCharacter)
        self._ui.selectAllHiraganaButton.clicked.connect(self.onSetAllHiraganaClicked)
        self._ui.selectNoneHiraganaButton.clicked.connect(self.onSetNoneHiraganaClicked)
        self._ui.selectAllKatakanaButton.clicked.connect(self.onSetAllKatakanaClicked)
        self._ui.selectNoneKatakanaButton.clicked.connect(self.onSetNoneKatakanaClicked)
        self._ui.oppositeKanaCheckbox.clicked.connect(self.onOppositeKanaCheckboxClicked)
        self._ui.oppositeKanaSpinBox.valueChanged.connect(self.onNumberChanged)
        self._ui.kanaTypeCombobox.currentIndexChanged.connect(self.onKanaTypeChanged)

        self.updateUi()

    def updateUi(self):
        idx = self._ui.kanaTypeCombobox.findText(self._kanaTrainerData.kanaType)
        if idx == -1:
            raise ValueError(self._kanaTrainerData.kanaType + u" Not found in combobox")
        self._ui.kanaTypeCombobox.setCurrentIndex(idx)
        self._ui.oppositeKanaCheckbox.setChecked(self._kanaTrainerData.showOppositeKana)
        self._ui.oppositeKanaSpinBox.setValue(self._kanaTrainerData.oppositeKanaStepSize)

    def onSetAllHiraganaClicked(self):
        self._kanaTrainerData.learnedHiragana.setAllLearned(True)

    def onSetNoneHiraganaClicked(self):
        self._kanaTrainerData.learnedHiragana.setAllLearned(False)

    def onSetAllKatakanaClicked(self):
        self._kanaTrainerData.learnedKatakana.setAllLearned(True)

    def onSetNoneKatakanaClicked(self):
        self._kanaTrainerData.learnedKatakana.setAllLearned(False)

    def onOppositeKanaCheckboxClicked(self):
        self._kanaTrainerData.showOppositeKana = self._ui.oppositeKanaCheckbox.isChecked()

    def onNumberChanged(self):
        self._kanaTrainerData.oppositeKanaStepSize = self._ui.oppositeKanaSpinBox.value()
        self._ui.label_5.setText(ordinal(self._ui.oppositeKanaSpinBox.value()) + u" card in ")

    def onKanaTypeChanged(self):
        if self._ui.kanaTypeCombobox.count() != 2:
            raise ValueError(u"Wrong item count in kana combobox")
        self._kanaTrainerData.kanaType = self._ui.kanaTypeCombobox.currentText()
        oppositeIndex = (self._ui.kanaTypeCombobox.currentIndex()+1) % 2
        self._ui.oppositeKanaLabel.setText(self._ui.kanaTypeCombobox.itemText(oppositeIndex))

    def closeEvent(self, qCloseEvent):
        self.accept()
        qCloseEvent.accept()

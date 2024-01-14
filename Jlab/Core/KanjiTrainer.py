from aqt.qt import *
from Core.KanjiTrainerData import *
from Core.KanjiTrainerUi import *
from Core.KanjiTools import *

class KanjiTrainer(QDialog):

    def __init__(self, kanjiTrainerData):
        assert isinstance(kanjiTrainerData, KanjiTrainerData)
        super(KanjiTrainer, self).__init__()

        self._kanjiTrainerData = kanjiTrainerData

        self._ui = Ui_KanjiTrainerUi()
        self._ui.setupUi(self)
        self._ui.heisigSpinBox.setMinimum(1)
        self._ui.heisigSpinBox.setMaximum(len(KanjiTools.heisigList))

        self._ui.heisigSpinBox.setValue(self._kanjiTrainerData.getHeisigIndex())
        self._ui.furiganaWithSpaceRadioButton.setChecked(self._kanjiTrainerData.displayType == KanjiTrainerData.DisplayType.furiganaWithSpace)
        self._ui.furiganaWithoutSpaceRadioButton.setChecked(self._kanjiTrainerData.displayType == KanjiTrainerData.DisplayType.furiganaWithoutSpace)
        self._ui.jlabRadioButton.setChecked(self._kanjiTrainerData.displayType == KanjiTrainerData.DisplayType.jlab)

        self._ui.furiganaWithSpaceRadioButton.clicked.connect(self.setDisplayType)
        self._ui.furiganaWithoutSpaceRadioButton.clicked.connect(self.setDisplayType)
        self._ui.jlabRadioButton.clicked.connect(self.setDisplayType)
        self._ui.heisigSpinBox.valueChanged.connect(self.setHeisigIndex)

    def setDisplayType(self):
        if self._ui.furiganaWithSpaceRadioButton.isChecked():
            self._kanjiTrainerData.displayType = KanjiTrainerData.DisplayType.furiganaWithSpace
        elif self._ui.furiganaWithoutSpaceRadioButton.isChecked():
            self._kanjiTrainerData.displayType = KanjiTrainerData.DisplayType.furiganaWithoutSpace
        elif self._ui.jlabRadioButton.isChecked():
            self._kanjiTrainerData.displayType = KanjiTrainerData.DisplayType.jlab
        else:
            raise ValueError("Unknown display type")

    def setHeisigIndex(self, heisigIndex):
        self._kanjiTrainerData.setHeisigIndex(heisigIndex)

    def closeEvent(self, qCloseEvent):
        self.accept()
        qCloseEvent.accept()

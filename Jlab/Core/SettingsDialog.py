from aqt.qt import *
from Core.SettingsDialogUi import *
from Core.ReadingAssistanceType import *
from Core.Settings import *
from Core.CardEndActionType import CardEndActionType
from Core.WebSearch import WebSearch
import os

class SettingsDialog(QDialog):
    def __init__(self, settings):
        super(SettingsDialog, self).__init__()
        self._ui = Ui_SettingsDialog()
        self._ui.setupUi(self)
        self._initComboboxes(settings)
        self._initManagementSettings(settings)
        self._ui.browseDataFolderButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        self._ui.browseDataFolderButton.clicked.connect(self.onBrowseClicked)
        self._ui.manualButton.clicked.connect(self.onManualClicked)

    def getDataFolder(self):
        return self._ui.dataFolderLineEdit.text()

    def setDataFolder(self, path):
        self._ui.dataFolderLineEdit.setText(path)

    def onBrowseClicked(self):
        self._ui.dataFolderLineEdit.setText(QFileDialog.getExistingDirectory(None, u"Select Directory"))

    def onManualClicked(self):
        WebSearch.openUrl("https://www.japanese-like-a-breeze.com/card-management/")

    def closeEvent(self, event):
        self.accept()

    def getSettings(self):
        result = Settings()
        result.listeningFrontReadingAssistance = self._ui.listeningFrontComboBox.currentText()
        result.listeningBackReadingAssistance = self._ui.listeningBackComboBox.currentText()
        result.clozeFrontReadingAssistance = self._ui.clozeFrontComboBox.currentText()
        result.clozeBackReadingAssistance = self._ui.clozeBackComboBox.currentText()
        result.clozeEditorReadingAssistance = self._ui.clozeEditorComboBox.currentText()
        result.manageJlabCards = self._ui.manageCheckbox.isChecked()
        result.promptBeforeCardManagementAction = self._ui.promptCheckbox.isChecked()
        result.endAction = self._ui.endActionComboBox.currentText()
        result.lcEndInterval =  self._ui.lcIntervalSpinBox.value()
        result.clozeEndInterval = self._ui.clozeIntervalSpinBox.value()
        return result

    def _initComboboxes(self, settings):
        self._initReadingAssistanceCombobox(self._ui.listeningFrontComboBox, settings.listeningFrontReadingAssistance)
        self._initReadingAssistanceCombobox(self._ui.listeningBackComboBox, settings.listeningBackReadingAssistance)
        self._initReadingAssistanceCombobox(self._ui.clozeFrontComboBox, settings.clozeFrontReadingAssistance)
        self._initReadingAssistanceCombobox(self._ui.clozeBackComboBox, settings.clozeBackReadingAssistance)
        self._initReadingAssistanceCombobox(self._ui.clozeEditorComboBox, settings.clozeEditorReadingAssistance)

    def _initReadingAssistanceCombobox(self, comboBox, value):
        comboBox.addItem(ReadingAssistanceType.latin)
        comboBox.addItem(ReadingAssistanceType.kanaTrainer)
        comboBox.addItem(ReadingAssistanceType.kanjiTrainer)
        comboBox.addItem(ReadingAssistanceType.none)
        self._setComboBoxIndexByText(comboBox, value)

    def _setComboBoxIndexByText(self, combobox, text):
        index = combobox.findText(text)
        if index == -1:
            raise ValueError(U"Item not found")
        combobox.setCurrentIndex(index)

    def _initManagementSettings(self, settings):
        self._ui.manageCheckbox.setChecked(settings.manageJlabCards)
        self._ui.promptCheckbox.setChecked(settings.promptBeforeCardManagementAction)

        self._ui.endActionComboBox.addItem(CardEndActionType.tag)
        self._ui.endActionComboBox.addItem(CardEndActionType.suspend)
        self._ui.endActionComboBox.addItem(CardEndActionType.delete)
        self._setComboBoxIndexByText(self._ui.endActionComboBox, settings.endAction)

        self._ui.lcIntervalSpinBox.setValue(settings.lcEndInterval)
        self._ui.clozeIntervalSpinBox.setValue(settings.clozeEndInterval)

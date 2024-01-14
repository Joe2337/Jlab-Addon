from Persistence.IStorable import *
from aqt.qt import *
from os import *
import os

import shutil

class UacError(Exception):
    def __init__(self):
        return

class SettingsPerApp(QObject, IStorable):
    loadedCustomFolderNotExisting = pyqtSignal()
    folderChanged = pyqtSignal()

    def __init__(self):
        super(QObject, self).__init__()
        self.version = 0
        self.dataFolder = u""

    def getDataFolder(self):
        if len(self.dataFolder) == 0 or not os.path.exists(self.dataFolder):
            raise ValueError(u"Data folder does not exist")
        return self.dataFolder

    def toDictionary(self):
        return {
            u"version" : self.version,
            u"identifier" : self.getIdentifier(),
            u"dataFolder" : self.dataFolder
        }

    def fromDictionary(self, dictionary):
        version = dictionary[u"version"]
        self.dataFolder = dictionary[u"dataFolder"]

        if len(self.dataFolder) != 0 and not os.path.isdir(self.dataFolder):
            self.loadedCustomFolderNotExisting.emit()
            return

        if len(self.dataFolder) != 0:
            self.folderChanged.emit()

    def setDataFolder(self, dataFolder):
        if len(dataFolder) == 0 or not os.path.isdir(dataFolder):
            raise ValueError(u"Data folder does not exist")

        if "program" in dataFolder.lower() or "windows" in dataFolder.lower(): #closest thing to platform independence, name depends on language: https://www.samlogic.net/articles/program-files-folder-different-languages.htm
            raise UacError()

        if dataFolder != self.dataFolder and os.path.isdir(self.dataFolder):
            for curSourceFile in os.listdir(self.dataFolder):
                curSourcePath = os.path.join(self.dataFolder, curSourceFile)
                if os.path.isdir(curSourcePath):
                    continue

                curTargetPath = os.path.join(dataFolder, curSourceFile)
                if not os.path.exists(curTargetPath):
                    shutil.copy(curSourcePath, curTargetPath)


        newFolder = self.dataFolder != dataFolder
        self.dataFolder = dataFolder
        if newFolder:
            self.folderChanged.emit()

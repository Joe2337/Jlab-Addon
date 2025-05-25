from Core.LearnedKanji import *
from Persistence.IStorable import *


class KanjiTrainerData(IStorable):
    class DisplayType:
        furiganaWithoutSpace = "Furigana"
        furiganaWithSpace = "FuriganaSpaced"
        jlab = "Jlab"

    def __init__(self):
        self.version = 0
        self._heisigIndex = 0
        self.displayType = KanjiTrainerData.DisplayType.furiganaWithSpace

        self.learnedKanji = LearnedKanji()  # this is not serialized, but computed

    def setHeisigIndex(self, heisigIndex):
        self._heisigIndex = heisigIndex
        self.learnedKanji.setHeisig(heisigIndex)

    def getHeisigIndex(self):
        return self._heisigIndex

    def toDictionary(self):
        return {"version": self.getVersion(), "identifier": self.getIdentifier(), "heisigIndex": self._heisigIndex, "displayType": self.displayType}

    def fromDictionary(self, dictionary):
        version = dictionary["version"]
        self.setHeisigIndex(dictionary["heisigIndex"])
        self.displayType = dictionary["displayType"]

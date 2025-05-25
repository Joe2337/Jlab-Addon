from Core.LearnedKana import *
from Core.KanaTools import *


class KanaTrainerData(IStorable):
    def __init__(self):
        self.version = 0

        self.learnedHiragana = LearnedKana()
        self.learnedHiragana.initHiragana()

        self.learnedKatakana = LearnedKana()
        self.learnedKatakana.initKatakana()

        self.kanaType = KanaType.hiragana
        self.showOppositeKana = False
        self.oppositeKanaStepSize = 2

    def toDictionary(self):
        return {
            "version": self.getVersion(),
            "identifier": self.getIdentifier(),
            "learnedHiragana": self.learnedHiragana.toDictionary(),
            "learnedKatakana": self.learnedKatakana.toDictionary(),
            "kanaType": self.kanaType,
            "showOppositeKana": self.showOppositeKana,
            "oppositeKanaStepSize": self.oppositeKanaStepSize,
        }

    def fromDictionary(self, dictionary):
        version = dictionary["version"]
        self.learnedHiragana.fromDictionary(dictionary["learnedHiragana"])
        self.learnedKatakana.fromDictionary(dictionary["learnedKatakana"])
        self.kanaType = dictionary["kanaType"]
        self.showOppositeKana = dictionary["showOppositeKana"]
        self.oppositeKanaStepSize = dictionary["oppositeKanaStepSize"]

    def getKanaTypeForDisplay(self, index):
        otherKana = KanaType.hiragana if self.kanaType == KanaType.katakana else KanaType.katakana
        if self.showOppositeKana and index % self.oppositeKanaStepSize == 0:
            return otherKana
        return self.kanaType

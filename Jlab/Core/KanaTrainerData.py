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
            u"version" : self.getVersion(),
            u"identifier" : self.getIdentifier(),
            u"learnedHiragana" : self.learnedHiragana.toDictionary(),
            u"learnedKatakana" : self.learnedKatakana.toDictionary(),
            u"kanaType" : self.kanaType,
            u"showOppositeKana" : self.showOppositeKana,
            u"oppositeKanaStepSize" : self.oppositeKanaStepSize
        }

    def fromDictionary(self, dictionary):
        version = dictionary[u"version"]
        self.learnedHiragana.fromDictionary(dictionary[u"learnedHiragana"])
        self.learnedKatakana.fromDictionary(dictionary[u"learnedKatakana"])
        self.kanaType = dictionary[u"kanaType"]
        self.showOppositeKana = dictionary[u"showOppositeKana"]
        self.oppositeKanaStepSize = dictionary[u"oppositeKanaStepSize"]

    def getKanaTypeForDisplay(self, index):
        otherKana = KanaType.hiragana if self.kanaType == KanaType.katakana else KanaType.katakana
        if self.showOppositeKana and index % self.oppositeKanaStepSize == 0:
            return otherKana
        return self.kanaType

from Core.KanjiTools import *

class LearnedKanji():
    def __init__(self):
        self._learnedKanji = set()
        self._learnedKanjiHeisig = set()
        self._customLearnedKanji = set()

    def setCustomLearnedKanji(self, customLearnedKanji):
        self._customLearnedKanji = customLearnedKanji
        self._updateLearnedKanji()

    def setHeisig(self, index):
        self._learnedKanjiHeisig = set()
        for i in range(0, index):
            self._learnedKanjiHeisig.add(KanjiTools.heisigList[i])
        self._updateLearnedKanji()

    def allKanjiLearned(self, string):
        for char in string:
            if char in KanjiTools.kanjiSet and not char in self._learnedKanji:
                return False
        return True

    def _updateLearnedKanji(self):
        self._learnedKanji = self._learnedKanjiHeisig.union(self._customLearnedKanji)

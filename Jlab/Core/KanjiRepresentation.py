from Core.LearnedKanji import *

# currently not used -> may be used in KanjiKanaTransliterator
class KanjiRepresentation:
    furiStart = "["
    furiEnd = "]"
    def __init__(self):
        self.furigana = ""
        self.jlab = ""

    def addNonKanjiText(self, nonKanjiText, fromLeft):
        if fromLeft:
            self.furigana += nonKanjiText
            self.jlab += nonKanjiText
        else:
            self.furigana = nonKanjiText + self.furigana
            self.jlab = nonKanjiText + self.jlab

    def addKanjiText(self, kanjiText, reading, learnedKanji, fromLeft):
        if fromLeft:
            if learnedKanji.allKanjiLearned(kanjiText):
                self.furigana += kanjiText
                self.jlab += kanjiText
            else:
                self.furigana += KanjiRepresentation.makeFurigana(kanjiText, reading)
                self.jlab += reading
        else:
            if learnedKanji.allKanjiLearned(kanjiText):
                self.furigana = kanjiText + self.furigana
                self.jlab = kanjiText + self.jlab
            else:
                self.furigana = KanjiRepresentation.makeFurigana(kanjiText, reading) + self.furigana
                self.jlab = reading + self.jlab

    def setKanjiText(self, kanjiText, reading, learnedKanji, fromLeft):
        if fromLeft:
            if learnedKanji.allKanjiLearned(kanjiText):
                self.furigana = kanjiText
                self.jlab = kanjiText
            else:
                self.furigana = KanjiRepresentation.makeFurigana(kanjiText, reading)
                self.jlab = reading
        else:
            if learnedKanji.allKanjiLearned(kanjiText):
                self.furigana = kanjiText
                self.jlab = kanjiText
            else:
                self.furigana = KanjiRepresentation.makeFurigana(kanjiText, reading)
                self.jlab = reading

    @staticmethod
    def makeFurigana(kanjiText, reading):
        # the space is required for proper formatting in Anki. without the space, anki adds furigana to
        # too many chars
        return " " + kanjiText + KanjiRepresentation.furiStart + reading + KanjiRepresentation.furiEnd
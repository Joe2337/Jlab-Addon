import unittest
from Core.LearnedKanji import *
from Core.KanjiRepresentation import *

class TestLearnedKanji(unittest.TestCase):

    def testLearnedKanji(self):
        learnedKanji = LearnedKanji()

        sequence = "こんにちは"
        self.assertTrue(learnedKanji.allKanjiLearned(sequence))

        sequence = "一ニ"
        self.assertFalse(learnedKanji.allKanjiLearned(sequence))

        learnedKanji.setHeisig(2)
        self.assertTrue(learnedKanji.allKanjiLearned(sequence))

        sequence = "一ニ巳"
        learnedKanji.setHeisig(len(KanjiTools.heisigList))
        self.assertTrue(learnedKanji.allKanjiLearned(sequence))

    def testRepresentation(self):
        learnedKanji = LearnedKanji()

        #non-learned kanji (furigana / reading should be shown)
        kanjiString = "一"
        reading = "a"
        representation = KanjiRepresentation()
        representation.addKanjiText(kanjiString, reading, learnedKanji, True)
        self.assertEqual(representation.jlab, reading)
        self.assertEqual(representation.furigana, KanjiRepresentation.makeFurigana(kanjiString, reading))

        #learned kanji  (furigana / reading should not be shown)
        learnedKanji.setHeisig(1)
        representation = KanjiRepresentation()
        representation.addKanjiText(kanjiString, reading, learnedKanji, True)
        self.assertEqual(representation.jlab, kanjiString)
        self.assertEqual(representation.furigana, kanjiString)

        #learned kanji plus additional non-kanji, which should not affect the representation
        kanjiString = "一あいうえお"
        reading = "a"
        representation = KanjiRepresentation()
        representation.addKanjiText(kanjiString, reading, learnedKanji, True)
        self.assertEqual(representation.jlab, kanjiString)
        self.assertEqual(representation.furigana, kanjiString)

        #non-learned kanji (furigana / reading should be shown)
        kanjiString = "食一"
        reading = "a"
        representation = KanjiRepresentation()
        representation.addKanjiText(kanjiString, reading, learnedKanji, True)
        self.assertEqual(representation.jlab, reading)
        self.assertEqual(representation.furigana, KanjiRepresentation.makeFurigana(kanjiString, reading))

        #set non-learned kanji as learned using the customLearnedKanji function (furigana / reading should be shown)
        learnedKanji.setCustomLearnedKanji(set('食'))
        representation = KanjiRepresentation()
        representation.addKanjiText(kanjiString, reading, learnedKanji, True)
        self.assertEqual(representation.jlab, kanjiString)
        self.assertEqual(representation.furigana, kanjiString)

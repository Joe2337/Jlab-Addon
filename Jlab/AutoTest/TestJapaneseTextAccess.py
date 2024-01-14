#coding: utf8

import unittest
from AutoTest.GlobalData import *

class TestJapaneseTextAccess(unittest.TestCase):

    # the test case just makes sure that no exceptions are thrown. It does not check the correctness of the actual
    # cloze positions.
    # Furigana requires special treatment, because its selection in anki is problematic: Selected text will contain
    # both the kanji and the furigana without brackets.
    def testClozeRetrievalFurigana(self):
            hiraText = u"たべる たべる"
            hiraClozeText = hiraText
            spacedKanjiText = u"食べる 食べる"
            kanjiClozeText = spacedKanjiText
            lemmata = u"食べる 食べる"

            # test case: multiple words, first word partially selected
            selectedText = u"食たべる"
            jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                             kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
            clozePositions = jTextAccess.getClozePositions(selectedText)

            hiraText = u"さつき おとうさん きゃらめる"
            hiraClozeText = hiraText
            spacedKanjiText = u"サツキ お父さん キャラメル"
            kanjiClozeText = spacedKanjiText
            lemmata = u"サツキ お父さん キャラメル"

            # test case: multiple words, first word partially selected
            selectedText = u"サツキ お父とうさん"
            jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                             kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
            clozePositions = jTextAccess.getClozePositions(selectedText)

    # the test case just makes sure that no exceptions are thrown. It does not check the correctness of the actual
    # cloze positions.
    def testClozeRetrieval(self):
        hiraText = u"ちがう もくてき もくてき"
        hiraClozeText = hiraText
        spacedKanjiText = u"違う 目的 目的"
        kanjiClozeText = spacedKanjiText
        lemmata = u"違う 目的"

        # ------------------------ kanji test cases ----------------------------------

        # test case: multiple words, first word partially selected
        selectedText = u"的 目的"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: multiple words, both words partially selected
        selectedText = u"的 目"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: multiple words, last word partially selected
        selectedText = u"目的 目"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single partial word end selected
        selectedText = u"的"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single partial word start selected
        selectedText = u"目"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single full word
        selectedText = u"違う"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: two full words
        selectedText = u"違う 目的"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: partial start word
        selectedText = u"う 目的"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # ------------------------ hiragana test cases ----------------------------------

        # test case: multiple words, first word partially selected
        selectedText = u"てき もくてき"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: multiple words, both words partially selected
        selectedText = u"てき もく"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: multiple words, last word partially selected
        selectedText = u"もくてき もく"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single partial word end selected
        selectedText = u"てき"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single partial word start selected
        selectedText = u"もく"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single full word
        selectedText = u"ちがう"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: two full words
        selectedText = u"ちがう もくてき"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: partial start word
        selectedText = u"う もくてき"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # ------------------------ roumaji test cases ----------------------------------

        # test case: multiple words, first word partially selected
        selectedText = u"てき もくてき"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, u"", False, False))

        # test case: multiple words, both words partially selected
        selectedText = u"てき もく"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, u"", False, False))

        # test case: multiple words, last word partially selected
        selectedText = u"もくてき もく"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, u"", False, False))

        # test case: single partial word end selected
        selectedText = u"てき"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, u"", False, False))

        # test case: single partial word start selected
        selectedText = u"もく"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, u"", False, False))

        # test case: single full word
        selectedText = u"ちがう"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, u"", False, False))

        # test case: two full words
        selectedText = u"ちがう もくてき"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, u"", False, False))

        # test case: partial start word
        selectedText = u"う もくてき"
        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, u"", False, False))

    def testTryMapTo(self):
        hiraText = u"ちがう もくてき もくてき"
        hiraClozeText = hiraText
        spacedKanjiText = u"違う 目的 目的"
        kanjiClozeText = spacedKanjiText
        lemmata = u"違う 目的"

        jTextAccess = JapaneseTextAccess(hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata,
                                         kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)

        self.assertEqual(jTextAccess.tryMapTo(u"ちがう", ReadingAssistanceType.latin), u"chigau")
        self.assertEqual(jTextAccess.tryMapTo(u"ちがう", ReadingAssistanceType.none), u"違う")
        self.assertEqual(jTextAccess.tryMapTo(u"ちがaう", ReadingAssistanceType.latin), u"ちがaう")
        self.assertEqual(jTextAccess.tryMapTo(u"ちがう も", ReadingAssistanceType.latin), u"chigau mo")
        self.assertEqual(jTextAccess.tryMapTo(u"ちがう もくてき", ReadingAssistanceType.latin), u"chigau mokuteki")
        self.assertEqual(jTextAccess.tryMapTo(u"てき", ReadingAssistanceType.latin), u"teki")

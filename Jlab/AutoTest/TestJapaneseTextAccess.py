# coding: utf8

import unittest
from AutoTest.GlobalData import *


class TestJapaneseTextAccess(unittest.TestCase):

    # the test case just makes sure that no exceptions are thrown. It does not check the correctness of the actual
    # cloze positions.
    # Furigana requires special treatment, because its selection in anki is problematic: Selected text will contain
    # both the kanji and the furigana without brackets.
    def testClozeRetrievalFurigana(self):
        hiraText = "たべる たべる"
        hiraClozeText = hiraText
        spacedKanjiText = "食べる 食べる"
        kanjiClozeText = spacedKanjiText
        lemmata = "食べる 食べる"

        # test case: multiple words, first word partially selected
        selectedText = "食たべる"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        hiraText = "さつき おとうさん きゃらめる"
        hiraClozeText = hiraText
        spacedKanjiText = "サツキ お父さん キャラメル"
        kanjiClozeText = spacedKanjiText
        lemmata = "サツキ お父さん キャラメル"

        # test case: multiple words, first word partially selected
        selectedText = "サツキ お父とうさん"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

    # the test case just makes sure that no exceptions are thrown. It does not check the correctness of the actual
    # cloze positions.
    def testClozeRetrieval(self):
        hiraText = "ちがう もくてき もくてき"
        hiraClozeText = hiraText
        spacedKanjiText = "違う 目的 目的"
        kanjiClozeText = spacedKanjiText
        lemmata = "違う 目的"

        # ------------------------ kanji test cases ----------------------------------

        # test case: multiple words, first word partially selected
        selectedText = "的 目的"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: multiple words, both words partially selected
        selectedText = "的 目"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: multiple words, last word partially selected
        selectedText = "目的 目"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single partial word end selected
        selectedText = "的"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single partial word start selected
        selectedText = "目"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single full word
        selectedText = "違う"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: two full words
        selectedText = "違う 目的"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: partial start word
        selectedText = "う 目的"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # ------------------------ hiragana test cases ----------------------------------

        # test case: multiple words, first word partially selected
        selectedText = "てき もくてき"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: multiple words, both words partially selected
        selectedText = "てき もく"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: multiple words, last word partially selected
        selectedText = "もくてき もく"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single partial word end selected
        selectedText = "てき"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single partial word start selected
        selectedText = "もく"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: single full word
        selectedText = "ちがう"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: two full words
        selectedText = "ちがう もくてき"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # test case: partial start word
        selectedText = "う もくてき"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(selectedText)

        # ------------------------ roumaji test cases ----------------------------------

        # test case: multiple words, first word partially selected
        selectedText = "てき もくてき"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, "", False, False))

        # test case: multiple words, both words partially selected
        selectedText = "てき もく"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, "", False, False))

        # test case: multiple words, last word partially selected
        selectedText = "もくてき もく"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, "", False, False))

        # test case: single partial word end selected
        selectedText = "てき"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, "", False, False))

        # test case: single partial word start selected
        selectedText = "もく"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, "", False, False))

        # test case: single full word
        selectedText = "ちがう"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, "", False, False))

        # test case: two full words
        selectedText = "ちがう もくてき"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, "", False, False))

        # test case: partial start word
        selectedText = "う もくてき"
        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )
        clozePositions = jTextAccess.getClozePositions(kanaRoumajiTransliterator.kanaToRoumaji(selectedText, "", False, False))

    def testTryMapTo(self):
        hiraText = "ちがう もくてき もくてき"
        hiraClozeText = hiraText
        spacedKanjiText = "違う 目的 目的"
        kanjiClozeText = spacedKanjiText
        lemmata = "違う 目的"

        jTextAccess = JapaneseTextAccess(
            hiraText, spacedKanjiText, hiraClozeText, kanjiClozeText, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False
        )

        self.assertEqual(jTextAccess.tryMapTo("ちがう", ReadingAssistanceType.latin), "chigau")
        self.assertEqual(jTextAccess.tryMapTo("ちがう", ReadingAssistanceType.none), "違う")
        self.assertEqual(jTextAccess.tryMapTo("ちがaう", ReadingAssistanceType.latin), "ちがaう")
        self.assertEqual(jTextAccess.tryMapTo("ちがう も", ReadingAssistanceType.latin), "chigau mo")
        self.assertEqual(jTextAccess.tryMapTo("ちがう もくてき", ReadingAssistanceType.latin), "chigau mokuteki")
        self.assertEqual(jTextAccess.tryMapTo("てき", ReadingAssistanceType.latin), "teki")

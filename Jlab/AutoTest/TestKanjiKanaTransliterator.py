#coding: utf8

import unittest
from AutoTest.GlobalData import *
from Core.KanjiKanaTransliterator import *
from Core.LearnedKanji import *

def checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraganaRemainder):
    if furigana != expectedFurigana:
        raise ValueError("Wrong furigana, expected: " + expectedFurigana + ", but is: " + furigana)
    if jlab != expectedJlab:
        raise ValueError("Wrong jlab, expected: " + expectedJlab + ", but is: " + jlab)
    if len(kanjiRemainder) != 0:
        raise ValueError("Kanji remainder not 0")
    if len(hiraganaRemainder) != 0:
        raise ValueError("Kana remainder not 0")

class TestKanjiKanaTransliteration(unittest.TestCase):

    def testWrongInputLength(self):
        print("AA")
        t = KanjiKanaTransliterator(kanjium, LearnedKanji())

        kanji = "xxx"
        kana = "xx"

        hiraStart, kanjiRemainder, hiraRemainter = t._splitToFirstKanji(kanji, kana, True)
        hiraStart, kanjiRemainder, hiraRemainter = t._splitToFirstKanji(kanji, kana, False)

    def testSplitBehavior(self):
        t = KanjiKanaTransliterator(kanjium, LearnedKanji())

        kanji = "x食y"
        kana = "xたy"

        hiraStart, kanjiRemainder, hiraRemainter = t._splitToFirstKanji(kanji, kana, True)
        self.assertEqual(hiraStart, "x")
        self.assertEqual(kanjiRemainder, "食y")
        self.assertEqual(hiraRemainter, "たy")

        hiraStart, kanjiRemainder, hiraRemainter = t._splitToFirstKanji(kanji, kana, False)
        self.assertEqual(hiraStart, "y")
        self.assertEqual(kanjiRemainder, "x食")
        self.assertEqual(hiraRemainter, "xた")


    def testSpellingCases(self):
        t = KanjiKanaTransliterator(kanjium, LearnedKanji())

        # unique reading found
        kanji = "食べる"
        kana = "たべる"
        expectedFurigana = " 食[た]べる"
        expectedJlab = "たべる"
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromLeft(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromLeft(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)

        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # reading not ok for single kanji: left should raise an exception, right should work
        kanji = "食べる"
        kana = "xべる"
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, False)
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, True)

        expectedFurigana = " 食[x]べる"
        expectedJlab = "xべる"
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)

        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # reading not ok for multiple kanji: left should raise an exception, right should work
        kanji = "食食べる"
        kana = "xxべる"
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, False)
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, True)

        expectedFurigana = " 食食[xx]べる"
        expectedJlab = "xxべる"
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)

        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # reading not ok for "in between"-kanji, no kana between kanji
        kanji = "食食べる"
        kana = "たxべる"
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, False)
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, True)

        expectedFurigana = " 食食[たx]べる"
        expectedJlab = "たxべる"
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)

        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # reading not ok for one kanji in a row of other kanji, should behave differently depending on defensiveness
        kanji = "食食べる"
        kana = "xたべる"
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, False)
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, True)

        expectedFurigana = " 食食[xた]べる"
        expectedJlab = "xたべる"
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")

        expectedFurigana = " 食[x] 食[た]べる"
        expectedJlab = "xたべる"
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromRight(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, kanjiRemainder, hiraRemainder)
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # reading not ok for one kanji among others in the word, separated by kana
        kanji = "食の食べる"
        kana = "たのxべる"
        expectedFurigana = " 食[た]の 食[x]べる"
        expectedJlab = "たのxべる"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")

        # make sure, that from left keeps stuff separated by kana
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromLeft(kanji, kana, True)
        self.assertEqual(furigana, " 食[た]の")
        self.assertEqual(jlab, "たの")
        self.assertEqual(kanjiRemainder, "食べる")
        self.assertEqual(hiraRemainder, "xべる")
        furigana, jlab, kanjiRemainder, hiraRemainder = t._transliterateWordFromLeft(kanji, kana, False)
        self.assertEqual(furigana, " 食[た]の")
        self.assertEqual(jlab, "たの")
        self.assertEqual(kanjiRemainder, "食べる")
        self.assertEqual(hiraRemainder, "xべる")




    # for more info in these test cases, refer to https://japanese.stackexchange.com/questions/69521/reading-per-kanji-irregular-readings
    def testSelectedWords(self):
        t = KanjiKanaTransliterator(kanjium, LearnedKanji())

        # irregular reading, which can't be resolved correctly by matching from left, but by non-defensive matching from right.
        kanji = "曳子"
        kana = "ひきこ"
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, False)
        self.assertRaises(Exception, t._transliterateWordFromLeft, kanji, kana, True)

        expectedFurigana = " 曳子[ひきこ]"
        expectedJlab = "ひきこ"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")

        expectedFurigana = " 曳[ひき] 子[こ]"
        expectedJlab = "ひきこ"
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # irregular reading enclosed with kana
        kanji = "お兄さん"
        kana = "おにいさん"

        expectedFurigana = "お 兄[にい]さん"
        expectedJlab = "おにいさん"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # irregular reading not enclosed
        kanji = "今日"
        kana = "きょう"

        expectedFurigana = " 今日[きょう]"
        expectedJlab = "きょう"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # kanji word longer than its reading
        kanji = "大口魚"
        kana = "たら"

        expectedFurigana = " 大口魚[たら]"
        expectedJlab = "たら"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # 2 readings for 1 compound, this is easy (resolved by regular cases)
        kanji = "人気"
        kana = "にんき"

        expectedFurigana = " 人[にん] 気[き]"
        expectedJlab = "にんき"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        kana = "にんき"

        kana = "ひとけ"
        expectedFurigana = " 人[ひと] 気[け]"
        expectedJlab = "ひとけ"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # order of the readings mixed up
        kanji = "不忍"
        kana = "しのばず"

        expectedFurigana = " 不忍[しのばず]"
        expectedJlab = "しのばず"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # hidden kana (the second "no" cannot be mapped anywhere, in this case defensive would be better)
        kanji = "不忍池"
        kana = "しのばずのいけ"

        expectedFurigana = " 不忍池[しのばずのいけ]"
        expectedJlab = "しのばずのいけ"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")

        expectedFurigana = " 不忍[しのばずの] 池[いけ]" #this furigana is wrong
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # irregular reading (same as kyou)
        kanji = "忠実"
        kana = "まめ"

        expectedFurigana = " 忠実[まめ]"
        expectedJlab = "まめ"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # same word with irregular reading (mame / 忠実) repeated, defensive would be better here.
        kanji = "忠実忠実しい"
        kana = "まめまめしい"

        expectedFurigana = " 忠実忠実[まめまめ]しい"
        expectedJlab = "まめまめしい"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")

        expectedFurigana = " 忠実忠[まめ] 実[まめ]しい" #this furigana is wrong
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")



    # the number test case is only for completenes, it is basically covered by the other cases above.
    # Numbers spelled as numeric chars are not found in kanjium, but correctly mapped to hiragana by mecab.
    # Therefore, defensive transliteration assigns the reading to the full word, non-defensive yields the correct
    # furigana by matching from right (if the rightmost kanji can be resolved uniquely).
    def testNumbers(self):
        t = KanjiKanaTransliterator(kanjium, LearnedKanji())

        kanji = "1年"
        kana = "いちねん"

        expectedFurigana = " 1年[いちねん]"
        expectedJlab = "いちねん"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")

        expectedFurigana = "1 年[ねん]"
        expectedJlab = "1ねん"
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




    def testKatakana(self):
        t = KanjiKanaTransliterator(kanjium, LearnedKanji())

        # Plain katakana must not yield furigana
        kanji = "カタカナ"
        kana = "かたかな"
        expectedFurigana = "カタカナ"
        expectedJlab = "カタカナ"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




        # Katakana in combination with kanji must not yield furigana
        # kanji at right side
        kanji = "カタカナ食"
        kana = "かたかなた"
        expectedFurigana = "カタカナ 食[た]"
        expectedJlab = "カタカナた"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")

        # kanji at left side
        kanji = "食カタカナ"
        kana = "たかたかな"
        expectedFurigana = " 食[た]カタカナ"
        expectedJlab = "たカタカナ"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")

        # kanji with regular reading inside
        kanji = "カタカナ食カタカナ"
        kana = "かたかなたかたかな"
        expectedFurigana = "カタカナ 食[た]カタカナ"
        expectedJlab = "カタカナたカタカナ"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")


        # kanji with irregular reading inside
        kanji = "カタカナ食カタカナ"
        kana = "かたかなxかたかな"
        expectedFurigana = "カタカナ 食[x]カタカナ"
        expectedJlab = "カタカナxカタカナ"
        furigana, jlab = t._transliterateWord(kanji, kana, True)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")
        furigana, jlab = t._transliterateWord(kanji, kana, False)
        checkOutput(furigana, expectedFurigana, jlab, expectedJlab, "", "")




    # check, if every word of the dictionary can be mapped to a reading without exceptions
    def testDictionary(self):
        t = KanjiKanaTransliterator(kanjium, LearnedKanji())

        i = 0
        numErrors = 0
        #file = codecs.open(u"C:/Tmp/Debug.txt", u"w", u"utf-8")

        rxRoumaji = re.compile(u"[a-zA-Z\uff01-\uff5a\u0370-\u03ff]")  # matches latin, japanese latin, greek characters

        for row in jDict.getExpressionAndReadingOfAllEntries():

            if rxRoumaji.search(row[0]) or rxRoumaji.search(row[1]):
                i += 1
                continue

            allExpressions = row[0].split(u",")
            allReadings = row[1].split(u",")

            oneFound = False
            errorMessages = u""
            for curExpression in allExpressions:
                for curReading in allReadings:
                    try:
                        t._transliterateWord(curExpression.strip(), curReading.strip(), False)
                        oneFound = True
                        break
                    except Exception as e:
                        errorMessages += str(e) + u"\n"
                        pass
                if oneFound:
                    break

            if not oneFound:
                # file.write(errorMessages)
                # file.write(u"Readings: " + row[1] + u"\n")
                # file.write(u"Expressions: " + row[0] + u"\n")
                # file.write(u"\n")
                numErrors += 1

            i += 1

        self.assertEqual(numErrors, 0)


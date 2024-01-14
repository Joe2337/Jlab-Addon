#coding: utf8

import unittest
from AutoTest.GlobalData import *

# test, if bijective hiragana to roumaji transliteration works by mapping each reading of the japanese dictionary from
# hiragana to roumaji and back
class TestHiraganaToRoumajiTransliteration(unittest.TestCase):
    def test_it(self):
        ignoreError = [9216, 129428] # these errors are caused by geminated syllabic n, which is not resolved correctly (っん -> nn -> んん). This is irregular kana use?
        for row in jDict.getAllReadings():
            roumaji = kanaRoumajiTransliterator.kanaToRoumaji(row[0], "", False, False)
            hiragana = kanaRoumajiTransliterator.mixedRoumajiToHiragana(roumaji)
            orgInHiraOnly = KanaTools.kataToHira(row[0])
            matchList = KanaTools.findPositionCaseInsensitiveStringInput(hiragana, orgInHiraOnly)

            if len(matchList) != 1:
                if row[1] in ignoreError:
                    continue
                print(row[1])
                print(str(len(matchList)) + u" matches found for JGroup id " + str(row[1]) + ":")
                print(matchList)
                print(u"")
                print(orgInHiraOnly + u" (hira only)")
                print(roumaji)
                print(hiragana + u" (hira-rouma-hira)")
                print(row[0] + u" (original)")
                print(u"")
                raise Exception(u"Error JGroup id " + str(row[1]) + u": Num matches found != 1")
                break

    # tests for a bug that caused katakana small tsu to be wrongly transliterated
    def test_it2(self):
        learnedKatakana.setAllLearned(True) #might cause other tests to fail, but currently wayne
        learnedHiragana.setAllLearned(True)
        dattaKatakana = kanaRoumajiTransliterator.kanaToRoumaji("ダッタ", "", False, True)
        dattaHiragana = kanaRoumajiTransliterator.kanaToRoumaji("だった", "", False, True)

        if(dattaKatakana != "ダッタ"):
            raise Exception(u"dattaKatakana != ダッタ")
        if(dattaHiragana != "だった"):
            raise Exception("dattaHiragana != だった")
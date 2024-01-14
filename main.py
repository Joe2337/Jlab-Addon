#coding: utf8
from Core.ClozeEditor import *
from Core.KanaTrainer import *
from Core.Kanjium import *
from Core.LearnedKana import *
from Dict.JapaneseDictionary import *
from Persistence.FileStorageEngine import *
from Core.SettingsDialog import *
from Core.SettingsPerApp import *
from Core.WebSearch import WebSearch
from Core.KanjiTrainerData import *
from Core.KanjiTrainer import *
import sys
import codecs
import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication

fileStorageEngine = FileStorageEngine()
kanaTrainerData = KanaTrainerData()
learnedHiragana = kanaTrainerData.learnedHiragana
learnedKatakana = kanaTrainerData.learnedKatakana
kanjiTrainerData = KanjiTrainerData()

kanaRoumajiTransliterator = KanaRoumajiTransliterator(learnedHiragana, learnedKatakana)
jDict = JapaneseDictionary()
kanjium = Kanjium()

kanjiKanaTransliterator = KanjiKanaTransliterator(kanjium, LearnedKanji())

def testClozeEditor():
    app = QApplication(sys.argv)

    # spacedKanji = u"なんだ 言いたい こと が ある なら 飲み込んで から 言えよ"
    # hiragana = u"なんだ いいたい こと が ある なら のみこんで から いえよ"
    # hiraganaCloze = hiragana
    # kanjiCloze = spacedKanji
    # lemmata = u"と が ある だ 飲み込む から"
    # selectedText = u"飲み込んで"

    spacedKanji = u"なんで 今日 は こんな 起こし方 すん の"
    hiragana = u"なんで きょう は こんな おこしかた すん の"
    hiraganaCloze = hiragana
    kanjiCloze = spacedKanji
    lemmata = u"なんで 今日 は こんな 起こす方 する の"
    selectedText = u"起こす"

    japaneseTextAccess = JapaneseTextAccess(hiragana, spacedKanji, hiraganaCloze, kanjiCloze, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, False)
    ex = ClozeEditor(japaneseTextAccess, selectedText, learnedHiragana, learnedKatakana, kanaRoumajiTransliterator, jDict, kanjium, ReadingAssistanceType.none)
    ex.resize(800, 800)
    ex.show()
    app.exec_()
    ex = None #this explicitly deletes all objects referenced by Qt and avoids memory leaks.
    print('\n'.join(repr(w) for w in app.allWidgets()))

def testKanaTrainer():
    app = QtWidgets.QApplication(sys.argv)

    try:
        fileStorageEngine.load(kanaTrainerData, u"C:/Tmp/", u"KanaTrainer")
    except:
        pass

    kanaTrainer = KanaTrainer(kanaTrainerData)
    result = kanaTrainer.exec()
    print(result)
    if result == 1:
        fileStorageEngine.save(kanaTrainerData, u"C:/Tmp/", u"KanaTrainer")

def testSettingsDialog():
    app = QtWidgets.QApplication(sys.argv)

    oldSettings = Settings()
    try:
        fileStorageEngine.load(oldSettings, u"C:/Tmp/", u"Settings")
    except:
        pass

    settingsDialog = SettingsDialog(oldSettings)

    print(settingsDialog.exec())

    newSettings = settingsDialog.getSettings()
    print(u"card format changed: " + str(oldSettings.cardFormatChanged(newSettings)))

    fileStorageEngine.save(newSettings, u"C:/Tmp/", u"Settings")

def testTransliteratorHiraToRouma():
    cs = TextFormatter.clozeStart
    ce = TextFormatter.clozeEnd

    print(kanaRoumajiTransliterator.transliterateCard(u"ソレ ハ " + cs + u"unverhofftes Glück (ein glücklicher Zufall )" + ce, u"それ は 棚ぼた", True, True))
    print(kanaRoumajiTransliterator.transliterateCard(u"あっ " + cs + u"to drop; to lose to leave behind" + ce + u" よ", u"あっ 落としました よ", True, True))

    cloze = cs + u"awf" + ce
    print(kanaRoumajiTransliterator.transliterateCard(u"は " + cloze + u" は " + cloze, u"は は A は", True, True))
    print(kanaRoumajiTransliterator.transliterateCard(u"は " + cloze + u" は " + cloze, u"は は A", True, True))

    print(kanaRoumajiTransliterator.transliterateCard(u"でぃてーる", u"でぃてーる", True, True))
    print(kanaRoumajiTransliterator.transliterateCard(u"は", u"は", True, True))
    print(kanaRoumajiTransliterator.kanaToRoumaji(u"がぎぐげござじずぜぞだぢづでどばぱびぴぶぷべぺぼぽ・きゃきゅきょしゃしゅしょちゃちゅちょにゃにゅにょひゃひゅひょみゃみゅみょりゃりゅ", u"", False, True))
    print(kanaRoumajiTransliterator.kanaToRoumaji(u"もう かのじょ と いう か お よめさん が ほしい わすれっぽい はっきり きょう　", u"A", True, True))
    print(kanaRoumajiTransliterator.kanaToRoumaji(KanaTools.hiraToKata(u"もう かのじょ と いう か お よめさん が ほしい としごろ な ん だ よ ね"), "A", True, True))

def testKanjium():
    readings = kanjium.getReadings(u"行")
    for curReading in readings:
        print(curReading)
    kanjium.countReadings()

def test_it():
    input = u"っん"
    roumaji = kanaRoumajiTransliterator.kanaToRoumaji(input, "", False, False)
    hiragana = kanaRoumajiTransliterator.mixedRoumajiToHiragana(roumaji)

    print(hiragana)
    print(input)

def testWebsearch():
    import time
    WebSearch.googleForGrammar(u"ます")
    time.sleep(2)
    WebSearch.googleTranslate(u"パンダは腸が短くて竹からだとあまり栄養がとれないんです")
    time.sleep(2)
    WebSearch.jgram(u"naru")
    time.sleep(2)
    WebSearch.verbixConjugate(u"食べる")
    time.sleep(2)
    WebSearch.verbixDeinflect(u"tabemasu")

def writeUpdateInfo():
    from Core.UpdateInformation import UpdateInformation
    u = UpdateInformation()
    fileStorageEngine.save(u, u"C:/Tmp/", u"UpdateInformation")

def testKanjiTrainer():
    app = QtWidgets.QApplication(sys.argv)

    try:
        fileStorageEngine.load(kanjiTrainerData, u"C:/Tmp/", u"KanjiTrainer")
    except:
        pass

    kanjiTrainer = KanjiTrainer(kanjiTrainerData)
    result = kanjiTrainer.exec()
    print(result)
    if result == 1:
        fileStorageEngine.save(kanjiTrainerData, u"C:/Tmp/", u"KanjiTrainer")

def affe(ok):
    print("load: " + str(ok))

import base64
import subprocess

from Persistence.FileStorageEngine import *
from Core.ClozeEditor import *
from Core.Kanjium import *
from Core.KanaTrainerData import *
from Core.LearnedKana import *
from Core.LearnedKanji import *
from Dict.JapaneseDictionary import *
from Core.KanjiKanaTransliterator import *
def main():
    lk = LearnedKanji()
    lk.setHeisig(1)
    t = KanjiKanaTransliterator(kanjium, lk)

    kanji = "‪2000年 前 の こと‬"
    kana = "2000ねん まえ の こと"
    # print(':'.join(hex(ord(x))[2:] for x in kanji))
    # return
    t.transliterateSentence(kanji, kana, True, False)
    return

    #writeUpdateInfo()
    #testKanaTrainer()
    #testKanjium()
    #testClozeEditor()
    #testSettingsDialog()
    #testWebsearch()
    testKanjiTrainer()

if __name__ == '__main__':
    sys.exit(main())
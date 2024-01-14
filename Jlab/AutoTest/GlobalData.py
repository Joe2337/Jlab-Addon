from Persistence.FileStorageEngine import *
from Core.ClozeEditor import *
from Core.Kanjium import *
from Core.KanaTrainerData import *
from Core.LearnedKana import *
from Core.LearnedKanji import *
from Dict.JapaneseDictionary import *

fileStorageEngine = FileStorageEngine()
kanaTrainerData = KanaTrainerData()
learnedHiragana = kanaTrainerData.learnedHiragana
learnedKatakana = kanaTrainerData.learnedKatakana

kanjium = Kanjium()
jDict = JapaneseDictionary()

kanaRoumajiTransliterator = KanaRoumajiTransliterator(learnedHiragana, learnedKatakana)
kanjiKanaTransliterator = KanjiKanaTransliterator(kanjium, LearnedKanji())

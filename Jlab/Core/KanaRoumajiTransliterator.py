#coding: utf8
from Core.KanaTools import *
from Dict.TextFormatter import *

# Parts of the parsing code within this file is adapted from jisho.org, here's Kim's original license:
# The MIT License (MIT)
# Copyright © 2015 Kim Ahlström <kim.ahlstrom@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

class KanaRoumajiTransliterator:
    # helper function for word-wise transliteration. This treats 1-char-hiragana-words as particles and spells them
    # differently, if modified hepburn should be used (i.e. ha -> wa, wo -> o). Works only, if the amount of words
    # in kanaInput and originalInput is the same (i.e. fails, if kanaInput contains a close that spans multiple words).
    # In this case, modified hepburn romanization may not be correct.
    def transliterateCard(self, kanaInput, originalInput, modifiedHepburn, useLearnedKana):
        cleanedClozeData = TextFormatter.replaceClozesWithPlaceholder(kanaInput) #replace all clozes with *

        kanaInput = cleanedClozeData[0]
        inputWords = kanaInput.split(u" ")
        originalWords = originalInput.split(u" ")

        result = ""
        if len(inputWords) != len(originalWords) or len(inputWords) == 1 and len(originalWords) == 1:
            result = self.kanaToRoumaji(kanaInput, originalInput, modifiedHepburn, useLearnedKana)
        else:
            for i, t in enumerate(inputWords):
                result += self.kanaToRoumaji(t, originalWords[i], modifiedHepburn, useLearnedKana)
                if i < len(inputWords) - 1:
                    result += " "

        return TextFormatter.replacePlaceholdersWithClozes(result, cleanedClozeData[1])

    # Converts Hiragana/Katakana to Roumaji
    # Can be applied sentence- and wordwise. If a character cannot be converted, it is adopted unchanged.
    # If applied word-wise, the original word can be supplied, which is then used for guessing the part-of-speech.
    # This is only required for hepburn-romanization though.
    # param originalInput: Optional parameter that can be used when applying the transliteration word-wise.
    # If this is the case, supply the original word in native script (i.e. with kanji). Supply "" if unknown. The word
    # will be used for guessing the part-of-speech
    # param learnedKana This must be either learned hiragana or katakana, depending on the type of kanaInput
    def kanaToRoumaji(self, kanaInput, originalInput, modifiedHepburn, useLearnedKana):
        if modifiedHepburn and len(originalInput) != 0 and not self._rxNoKana.search(originalInput):
            result = self._particleTrans.get(KanaTools.kataToHira(kanaInput), 0)
            if useLearnedKana and self.kanaLearned(kanaInput):
                return kanaInput
            if result != 0:
                return result

        result = ""
        geminate = False
        charsForConversion = ""

        lastSmallTsu = self._smallTsu
        while len(kanaInput) != 0:
            mora = ""

            #2 hira-chars have highest priority
            if len(kanaInput) >= 2:
                charsForConversion = kanaInput[:2]
                convertedChars = self._hiraToRouma.get(KanaTools.kataToHira(charsForConversion), 0)
                if convertedChars != 0:
                    mora = convertedChars

            #process 1 char, if no longer (2 char) mora was found
            if len(mora) == 0 and len(kanaInput) >= 1:
                charsForConversion = kanaInput[0]

                if KanaTools.kataToHira(charsForConversion) == self._smallTsu:
                    lastSmallTsu = charsForConversion #keeps hira / kata

                    if geminate: #keeps multiple small tsus
                        result += lastSmallTsu

                    geminate = True
                    kanaInput = kanaInput[1:]
                    continue
                elif (len(kanaInput) >= 2 and
                              KanaTools.kataToHira(charsForConversion) == self._syllabicN and
                              KanaTools.kataToHira(kanaInput[1]) in self._syllabicNDash):
                        mora = u"n'"
                else:
                    convertedChars = self._hiraToRouma.get(KanaTools.kataToHira(charsForConversion), 0)
                    if convertedChars != 0:
                        mora = convertedChars

            kanaCharsForDisplay = charsForConversion
            if geminate:
                geminate = False
                if len(mora) > 0:
                    mora = mora[0] + mora
                kanaCharsForDisplay = lastSmallTsu + charsForConversion

            if len(mora) > 0 and (not useLearnedKana or not self.kanaLearned(kanaCharsForDisplay)):
                result += mora
            else:
                result += kanaCharsForDisplay

            kanaInput = kanaInput[len(charsForConversion):]

        if geminate:
            result += self._smallTsu #this keeps a small tsu at the end of the string
        return result

    def mixedRoumajiToHiragana(self, mixedRoumajiInput):
        result = u""
        mixedRoumajiInput = KanaTools.kataToHira(mixedRoumajiInput)
        while len(mixedRoumajiInput) != 0:

            #first, check for double-characters inducing a small tsu
            if len(mixedRoumajiInput) >= 2:
                doubleChar = mixedRoumajiInput[:2].lower()
                if self._rxCharsToSmallTsu.search(doubleChar[0]) is not None and doubleChar[0] == doubleChar[1] and doubleChar[0] != u'n':
                    result += self._smallTsu
                    mixedRoumajiInput = mixedRoumajiInput[1:]
                    continue

            #second, replace all roumaji chars starting with the longest possible mora (length 3, 2, 1)
            moraFound = False
            for curMoraLength in range(3, 0, -1):
                if len(mixedRoumajiInput) < curMoraLength:
                    continue

                curMora = mixedRoumajiInput[:curMoraLength].lower()
                if self._rxNoRoumaji.search(curMora):
                    continue

                convertedMora = self._roumaToHira.get(curMora, 0)
                if convertedMora != 0:
                    moraFound = True
                    result += convertedMora
                    mixedRoumajiInput = mixedRoumajiInput[curMoraLength:]
                    break

            if not moraFound:
                result += mixedRoumajiInput[:1]
                mixedRoumajiInput = mixedRoumajiInput[1:]

        return result


    def kanaLearned(self, kanaInput):
        return self._learnedHiragana.isLearned(kanaInput) or self._learnedKatakana.isLearned(kanaInput)

    def initRoumaToHira(self):
        self._roumaToHira = {}

        irrelevant = [u'ゖ', u'ゎ', u'ぃ', u'ぅ', u'ぇ', u'ゕ', u'ぁ', u'ぉ']

        for hira, rouma in self._hiraToRouma.items():
            if hira in irrelevant:
                continue

            if rouma in self._roumaToHira.keys():
                raise Exception("Multiple mappings found")
            else:
                self._roumaToHira[rouma] = hira

        self._roumaToHira[u"n'"] = u"ん"

        # for rouma, hira in self._roumaToHira.items():
        #     print(rouma + " - " + hira)

    def __init__(self, learnedHiragana, learnedKatakana):
        self._learnedHiragana = learnedHiragana
        self._learnedKatakana = learnedKatakana

        #Matches everything but kana-letters. Also Whitespaces!
        self._rxNoKana = re.compile(u"[^ぁ-ゖァ-ー]")

        #Matches everything but letters relevant for roumaji-to-hiragana conversion
        self._rxNoRoumaji = re.compile(u"[^A-Za-z\-']")

        self._rxCharsToSmallTsu = re.compile(u"[kgsztdnbpmyrlwchfj]")

        self._smallTsu = u"っ"
        self._syllabicN = u"ん"
        self._particleTrans = {
            u"は": u"wa",
            u"を": u"o",
            u"へ": u"e"
        }
        self._syllabicNDash = {u"や", u"ゆ", u"よ", u"あ", u"い", u"う", u"え", u"お"}

        # Ambiguities are: ji (じ / ぢ), zu (ず / づ) and ja/ju/jo (standard is: (じゃ　じゅ　じょ), (ぢゃ　ぢゅ　ぢょ) are unkommon)
        # they are resolved by: {dji, dzu, dja, dju, djo}. See https://www.nayuki.io/page/variations-on-japanese-romanization
        # this is uncommon though?
        self._hiraToRouma = {
            u"あ": u"a",
            u"い": u"i",
            u"う": u"u",
            u"え": u"e",
            u"お": u"o",
            u"か": u"ka",
            u"き": u"ki",
            u"く": u"ku",
            u"け": u"ke",
            u"こ": u"ko",
            u"が": u"ga",
            u"ぎ": u"gi",
            u"ぐ": u"gu",
            u"げ": u"ge",
            u"ご": u"go",
            u"さ": u"sa",
            u"し": u"shi",
            u"す": u"su",
            u"せ": u"se",
            u"そ": u"so",
            u"ざ": u"za",
            u"じ": u"ji",
            u"ず": u"zu",
            u"ぜ": u"ze",
            u"ぞ": u"zo",
            u"た": u"ta",
            u"ち": u"chi",
            u"つ": u"tsu",
            u"て": u"te",
            u"と": u"to",
            u"だ": u"da",
            u"ぢ": u"dji",
            u"づ": u"dzu",
            u"で": u"de",
            u"ど": u"do",
            u"な": u"na",
            u"に": u"ni",
            u"ぬ": u"nu",
            u"ね": u"ne",
            u"の": u"no",
            u"は": u"ha",
            u"ひ": u"hi",
            u"ふ": u"fu",
            u"へ": u"he",
            u"ほ": u"ho",
            u"ば": u"ba",
            u"び": u"bi",
            u"ぶ": u"bu",
            u"べ": u"be",
            u"ぼ": u"bo",
            u"ぱ": u"pa",
            u"ぴ": u"pi",
            u"ぷ": u"pu",
            u"ぺ": u"pe",
            u"ぽ": u"po",
            u"ま": u"ma",
            u"み": u"mi",
            u"む": u"mu",
            u"め": u"me",
            u"も": u"mo",
            u"や": u"ya",
            u"ゆ": u"yu",
            u"よ": u"yo",
            u"ら": u"ra",
            u"り": u"ri",
            u"る": u"ru",
            u"れ": u"re",
            u"ろ": u"ro",
            u"わ": u"wa",
            u"うぃ": u"whi",
            u"うぇ": u"whe",
            u"を": u"wo",
            u"ゑ": u"we",
            u"ゐ": u"wi",
            u"ー": u"-",
            u"ん": u"n",
            u"きゃ": u"kya",
            u"きゅ": u"kyu",
            u"きょ": u"kyo",
            u"きぇ": u"kye",
            u"きぃ": u"kyi",
            u"ぎゃ": u"gya",
            u"ぎゅ": u"gyu",
            u"ぎょ": u"gyo",
            u"ぎぇ": u"gye",
            u"ぎぃ": u"gyi",
            u"くぁ": u"kwa",
            u"くぃ": u"kwi",
            u"くぅ": u"kwu",
            u"くぇ": u"kwe",
            u"くぉ": u"kwo",
            u"ぐぁ": u"qwa",
            u"ぐぃ": u"gwi",
            u"ぐぅ": u"gwu",
            u"ぐぇ": u"gwe",
            u"ぐぉ": u"gwo",
            u"しゃ": u"sha",
            u"しぃ": u"syi",
            u"しゅ": u"shu",
            u"しぇ": u"she",
            u"しょ": u"sho",
            u"じゃ": u"ja",
            u"じゅ": u"ju",
            u"じぇ": u"jye",
            u"じょ": u"jo",
            u"じぃ": u"jyi",
            u"すぁ": u"swa",
            u"すぃ": u"swi",
            u"すぅ": u"swu",
            u"すぇ": u"swe",
            u"すぉ": u"swo",
            u"ちゃ": u"cha",
            u"ちゅ": u"chu",
            u"ちぇ": u"tye",
            u"ちょ": u"cho",
            u"ちぃ": u"tyi",
            u"ぢゃ": u"dja",
            u"ぢぃ": u"dyi",
            u"ぢゅ": u"dju",
            u"ぢぇ": u"dye",
            u"ぢょ": u"djo",
            u"つぁ": u"tsa",
            u"つぃ": u"tsi",
            u"つぇ": u"tse",
            u"つぉ": u"tso",
            u"てゃ": u"tha",
            u"てぃ": u"thi",
            u"てゅ": u"thu",
            u"てぇ": u"the",
            u"てょ": u"tho",
            u"とぁ": u"twa",
            u"とぃ": u"twi",
            u"とぅ": u"twu",
            u"とぇ": u"twe",
            u"とぉ": u"two",
            u"でゃ": u"dha",
            u"でぃ": u"dhi",
            u"でゅ": u"dhu",
            u"でぇ": u"dhe",
            u"でょ": u"dho",
            u"どぁ": u"dwa",
            u"どぃ": u"dwi",
            u"どぅ": u"dwu",
            u"どぇ": u"dwe",
            u"どぉ": u"dwo",
            u"にゃ": u"nya",
            u"にゅ": u"nyu",
            u"にょ": u"nyo",
            u"にぇ": u"nye",
            u"にぃ": u"nyi",
            u"ひゃ": u"hya",
            u"ひぃ": u"hyi",
            u"ひゅ": u"hyu",
            u"ひぇ": u"hye",
            u"ひょ": u"hyo",
            u"びゃ": u"bya",
            u"びぃ": u"byi",
            u"びゅ": u"byu",
            u"びぇ": u"bye",
            u"びょ": u"byo",
            u"ぴゃ": u"pya",
            u"ぴぃ": u"pyi",
            u"ぴゅ": u"pyu",
            u"ぴぇ": u"pye",
            u"ぴょ": u"pyo",
            u"ふぁ": u"fwa",
            u"ふぃ": u"fyi",
            u"ふぇ": u"fye",
            u"ふぉ": u"fwo",
            u"ふぅ": u"fwu",
            u"ふゃ": u"fya",
            u"ふゅ": u"fyu",
            u"ふょ": u"fyo",
            u"みゃ": u"mya",
            u"みぃ": u"myi",
            u"みゅ": u"myu",
            u"みぇ": u"mye",
            u"みょ": u"myo",
            u"りゃ": u"rya",
            u"りぃ": u"ryi",
            u"りゅ": u"ryu",
            u"りぇ": u"rye",
            u"りょ": u"ryo",
            u"ゔぁ": u"va",
            u"ゔぃ": u"vyi",
            u"ゔ": u"vu",
            u"ゔぇ": u"vye",
            u"ゔぉ": u"vo",
            u"ゔゃ": u"vya",
            u"ゔゅ": u"vyu",
            u"ゔょ": u"vyo",
            u"うぁ": u"wha",
            u"いぇ": u"ye",
            u"うぉ": u"who",
            u"ぁ": u"a",
            u"ぃ": u"i",
            u"ぅ": u"u",
            u"ぇ": u"e",
            u"ぉ": u"o",
            u"ゕ": u"ka",
            u"ゖ": u"ke",
            u"ゎ": u"wa"
        }

        self.initRoumaToHira()
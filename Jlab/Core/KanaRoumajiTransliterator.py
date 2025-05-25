# coding: utf8
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
        cleanedClozeData = TextFormatter.replaceClozesWithPlaceholder(kanaInput)  # replace all clozes with *

        kanaInput = cleanedClozeData[0]
        inputWords = kanaInput.split(" ")
        originalWords = originalInput.split(" ")

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

            # 2 hira-chars have highest priority
            if len(kanaInput) >= 2:
                charsForConversion = kanaInput[:2]
                convertedChars = self._hiraToRouma.get(KanaTools.kataToHira(charsForConversion), 0)
                if convertedChars != 0:
                    mora = convertedChars

            # process 1 char, if no longer (2 char) mora was found
            if len(mora) == 0 and len(kanaInput) >= 1:
                charsForConversion = kanaInput[0]

                if KanaTools.kataToHira(charsForConversion) == self._smallTsu:
                    lastSmallTsu = charsForConversion  # keeps hira / kata

                    if geminate:  # keeps multiple small tsus
                        result += lastSmallTsu

                    geminate = True
                    kanaInput = kanaInput[1:]
                    continue
                elif (
                    len(kanaInput) >= 2
                    and KanaTools.kataToHira(charsForConversion) == self._syllabicN
                    and KanaTools.kataToHira(kanaInput[1]) in self._syllabicNDash
                ):
                    mora = "n'"
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

            kanaInput = kanaInput[len(charsForConversion) :]

        if geminate:
            result += self._smallTsu  # this keeps a small tsu at the end of the string
        return result

    def mixedRoumajiToHiragana(self, mixedRoumajiInput):
        result = ""
        mixedRoumajiInput = KanaTools.kataToHira(mixedRoumajiInput)
        while len(mixedRoumajiInput) != 0:

            # first, check for double-characters inducing a small tsu
            if len(mixedRoumajiInput) >= 2:
                doubleChar = mixedRoumajiInput[:2].lower()
                if self._rxCharsToSmallTsu.search(doubleChar[0]) is not None and doubleChar[0] == doubleChar[1] and doubleChar[0] != "n":
                    result += self._smallTsu
                    mixedRoumajiInput = mixedRoumajiInput[1:]
                    continue

            # second, replace all roumaji chars starting with the longest possible mora (length 3, 2, 1)
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

        irrelevant = ["ゖ", "ゎ", "ぃ", "ぅ", "ぇ", "ゕ", "ぁ", "ぉ"]

        for hira, rouma in self._hiraToRouma.items():
            if hira in irrelevant:
                continue

            if rouma in self._roumaToHira.keys():
                raise Exception("Multiple mappings found")
            else:
                self._roumaToHira[rouma] = hira

        self._roumaToHira["n'"] = "ん"

        # for rouma, hira in self._roumaToHira.items():
        #     print(rouma + " - " + hira)

    def __init__(self, learnedHiragana, learnedKatakana):
        self._learnedHiragana = learnedHiragana
        self._learnedKatakana = learnedKatakana

        # Matches everything but kana-letters. Also Whitespaces!
        self._rxNoKana = re.compile("[^ぁ-ゖァ-ー]")

        # Matches everything but letters relevant for roumaji-to-hiragana conversion
        self._rxNoRoumaji = re.compile("[^A-Za-z\-']")

        self._rxCharsToSmallTsu = re.compile("[kgsztdnbpmyrlwchfj]")

        self._smallTsu = "っ"
        self._syllabicN = "ん"
        self._particleTrans = {"は": "wa", "を": "o", "へ": "e"}
        self._syllabicNDash = {"や", "ゆ", "よ", "あ", "い", "う", "え", "お"}

        # Ambiguities are: ji (じ / ぢ), zu (ず / づ) and ja/ju/jo (standard is: (じゃ　じゅ　じょ), (ぢゃ　ぢゅ　ぢょ) are unkommon)
        # they are resolved by: {dji, dzu, dja, dju, djo}. See https://www.nayuki.io/page/variations-on-japanese-romanization
        # this is uncommon though?
        self._hiraToRouma = {
            "あ": "a",
            "い": "i",
            "う": "u",
            "え": "e",
            "お": "o",
            "か": "ka",
            "き": "ki",
            "く": "ku",
            "け": "ke",
            "こ": "ko",
            "が": "ga",
            "ぎ": "gi",
            "ぐ": "gu",
            "げ": "ge",
            "ご": "go",
            "さ": "sa",
            "し": "shi",
            "す": "su",
            "せ": "se",
            "そ": "so",
            "ざ": "za",
            "じ": "ji",
            "ず": "zu",
            "ぜ": "ze",
            "ぞ": "zo",
            "た": "ta",
            "ち": "chi",
            "つ": "tsu",
            "て": "te",
            "と": "to",
            "だ": "da",
            "ぢ": "dji",
            "づ": "dzu",
            "で": "de",
            "ど": "do",
            "な": "na",
            "に": "ni",
            "ぬ": "nu",
            "ね": "ne",
            "の": "no",
            "は": "ha",
            "ひ": "hi",
            "ふ": "fu",
            "へ": "he",
            "ほ": "ho",
            "ば": "ba",
            "び": "bi",
            "ぶ": "bu",
            "べ": "be",
            "ぼ": "bo",
            "ぱ": "pa",
            "ぴ": "pi",
            "ぷ": "pu",
            "ぺ": "pe",
            "ぽ": "po",
            "ま": "ma",
            "み": "mi",
            "む": "mu",
            "め": "me",
            "も": "mo",
            "や": "ya",
            "ゆ": "yu",
            "よ": "yo",
            "ら": "ra",
            "り": "ri",
            "る": "ru",
            "れ": "re",
            "ろ": "ro",
            "わ": "wa",
            "うぃ": "whi",
            "うぇ": "whe",
            "を": "wo",
            "ゑ": "we",
            "ゐ": "wi",
            "ー": "-",
            "ん": "n",
            "きゃ": "kya",
            "きゅ": "kyu",
            "きょ": "kyo",
            "きぇ": "kye",
            "きぃ": "kyi",
            "ぎゃ": "gya",
            "ぎゅ": "gyu",
            "ぎょ": "gyo",
            "ぎぇ": "gye",
            "ぎぃ": "gyi",
            "くぁ": "kwa",
            "くぃ": "kwi",
            "くぅ": "kwu",
            "くぇ": "kwe",
            "くぉ": "kwo",
            "ぐぁ": "qwa",
            "ぐぃ": "gwi",
            "ぐぅ": "gwu",
            "ぐぇ": "gwe",
            "ぐぉ": "gwo",
            "しゃ": "sha",
            "しぃ": "syi",
            "しゅ": "shu",
            "しぇ": "she",
            "しょ": "sho",
            "じゃ": "ja",
            "じゅ": "ju",
            "じぇ": "jye",
            "じょ": "jo",
            "じぃ": "jyi",
            "すぁ": "swa",
            "すぃ": "swi",
            "すぅ": "swu",
            "すぇ": "swe",
            "すぉ": "swo",
            "ちゃ": "cha",
            "ちゅ": "chu",
            "ちぇ": "tye",
            "ちょ": "cho",
            "ちぃ": "tyi",
            "ぢゃ": "dja",
            "ぢぃ": "dyi",
            "ぢゅ": "dju",
            "ぢぇ": "dye",
            "ぢょ": "djo",
            "つぁ": "tsa",
            "つぃ": "tsi",
            "つぇ": "tse",
            "つぉ": "tso",
            "てゃ": "tha",
            "てぃ": "thi",
            "てゅ": "thu",
            "てぇ": "the",
            "てょ": "tho",
            "とぁ": "twa",
            "とぃ": "twi",
            "とぅ": "twu",
            "とぇ": "twe",
            "とぉ": "two",
            "でゃ": "dha",
            "でぃ": "dhi",
            "でゅ": "dhu",
            "でぇ": "dhe",
            "でょ": "dho",
            "どぁ": "dwa",
            "どぃ": "dwi",
            "どぅ": "dwu",
            "どぇ": "dwe",
            "どぉ": "dwo",
            "にゃ": "nya",
            "にゅ": "nyu",
            "にょ": "nyo",
            "にぇ": "nye",
            "にぃ": "nyi",
            "ひゃ": "hya",
            "ひぃ": "hyi",
            "ひゅ": "hyu",
            "ひぇ": "hye",
            "ひょ": "hyo",
            "びゃ": "bya",
            "びぃ": "byi",
            "びゅ": "byu",
            "びぇ": "bye",
            "びょ": "byo",
            "ぴゃ": "pya",
            "ぴぃ": "pyi",
            "ぴゅ": "pyu",
            "ぴぇ": "pye",
            "ぴょ": "pyo",
            "ふぁ": "fwa",
            "ふぃ": "fyi",
            "ふぇ": "fye",
            "ふぉ": "fwo",
            "ふぅ": "fwu",
            "ふゃ": "fya",
            "ふゅ": "fyu",
            "ふょ": "fyo",
            "みゃ": "mya",
            "みぃ": "myi",
            "みゅ": "myu",
            "みぇ": "mye",
            "みょ": "myo",
            "りゃ": "rya",
            "りぃ": "ryi",
            "りゅ": "ryu",
            "りぇ": "rye",
            "りょ": "ryo",
            "ゔぁ": "va",
            "ゔぃ": "vyi",
            "ゔ": "vu",
            "ゔぇ": "vye",
            "ゔぉ": "vo",
            "ゔゃ": "vya",
            "ゔゅ": "vyu",
            "ゔょ": "vyo",
            "うぁ": "wha",
            "いぇ": "ye",
            "うぉ": "who",
            "ぁ": "a",
            "ぃ": "i",
            "ぅ": "u",
            "ぇ": "e",
            "ぉ": "o",
            "ゕ": "ka",
            "ゖ": "ke",
            "ゎ": "wa",
        }

        self.initRoumaToHira()

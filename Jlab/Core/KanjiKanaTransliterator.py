from Core.KanjiTools import *
from Core.Kanjium import *
from Core.KanjiRepresentation import *
from Dict.TextFormatter import *

# This class maps kanji within a word to their associated reading (both kanji and kana word must be given, which usually results from mecab).
# It is capable of creating two representations out of this. Furigana and the jlab kanji trainer's own representation.
# For furigana, the readings are attached to the kanji. If the kanji was learned, the reading is omitted.
# For jlab, the kana reading is replaced by the kanji.
# The class tries to map the readings to the smallest possible context (i.e. ideally, attaches a reading to each individual kanji).
# However, this is not always possible, see here why: https://japanese.stackexchange.com/questions/69521/reading-per-kanji-irregular-readings
# Therefore, a heuristic is used, which yields correct representations most of the time, but not always. It works as follows:
# - first, kana / kanji words are matched from left. Equal kana characters are consumed, Kanji are only consumed if they can be resolved by "official" readings
# - If the word can't be fully resolved from left, the remainders are resolved from right. From right works slightly different.
#   If remaining characters cannot be resolved, they are either used as reading for the remaining chars or as reading for the entire
#   chunk (defensive mode, see comment in transliterateFromRight)
#
# A more sophisticated solution could be https://github.com/Doublevil/JmdictFurigana
class KanjiKanaTransliterator:
    space = "\u205F" #http://jkorpela.fi/chars/spaces.html
    def __init__(self, kanjium, learnedKanji):
        assert isinstance(kanjium, Kanjium)
        self._kanjium = kanjium
        self._learnedKanji = learnedKanji

    def transliterateSentence(self, sentenceKanji, sentenceHiragana, defensively, spacedFurigana):
        cleanedClozeKanji = TextFormatter.replaceClozesWithPlaceholder(sentenceKanji) # replace all clozes with *
        cleanedClozeHiragana = TextFormatter.replaceClozesWithPlaceholder(sentenceHiragana)  # replace all clozes with *

        cleanedSentenceKanji = cleanedClozeKanji[0]
        kanjiWords = cleanedSentenceKanji.split(u" ")

        cleanedSentenceHiragana = cleanedClozeHiragana[0]
        hiraganaWords = cleanedSentenceHiragana.split(u" ")

        furiganaResult = jlabResult = ""
        if len(kanjiWords) != len(hiraganaWords):
            return sentenceKanji, sentenceHiragana
        else:
            for index, word in enumerate(kanjiWords):
                curKanjiWord = kanjiWords[index]
                curHiraganaWord = hiraganaWords[index]
                furigana, jlab = self._transliterateWord(kanjiWords[index], hiraganaWords[index], defensively)

                if index != 0:
                    # Anki's furigana requires furigana'ed char groups to be separated with a roman whitespace from preceding
                    # chars for correct rendering. The whitespace is then omitted. Unfortunately, all roman whitespaces
                    # are omitted, therefore I use a different space character, which is kept
                    # For other whitespaces, see http://jkorpela.fi/chars/spaces.html
                    if spacedFurigana:
                        furiganaResult += KanjiKanaTransliterator.space
                    jlabResult += " "

                if curKanjiWord == TextFormatter.clozePlaceholder:
                    furiganaResult += curKanjiWord
                    jlabResult += curHiraganaWord
                else:
                    furiganaResult += furigana
                    jlabResult += jlab

        furiganaResult = TextFormatter.replacePlaceholdersWithClozes(furiganaResult, cleanedClozeKanji[1])
        jlabResult = TextFormatter.replacePlaceholdersWithClozes(jlabResult, cleanedClozeKanji[1])
        return furiganaResult, jlabResult

    def getChars(self, kanjiWord, hiraganaWord, fromLeft, index):
        if fromLeft:
            return (kanjiWord[index], hiraganaWord[index])
        else:
            return (kanjiWord[-(index+1)], hiraganaWord[-(index+1)])

    # returns: hiragana start, kanji remainder, hiragana remainder
    def _splitToFirstKanji(self, kanjiWord, hiraganaWord, fromLeft):
        for i in range(0, min(len(hiraganaWord), len(kanjiWord))):
            charTuple = self.getChars(kanjiWord, hiraganaWord, fromLeft, i)
            if KanaTools.kataToHira(charTuple[0]) != charTuple[1]:
                if fromLeft:
                    return kanjiWord[:i], kanjiWord[i:], hiraganaWord[i:]
                else:
                    return kanjiWord[len(kanjiWord)-i:], kanjiWord[:len(kanjiWord)-i], hiraganaWord[:len(hiraganaWord)-i]

        return "", kanjiWord, hiraganaWord

    def _getReadingForFirstKanji(self, kanji, hiraganaString, fromLeft):
        readings = self._kanjium.getReadings(kanji)

        result = ""
        for curReading in readings:
            if fromLeft and hiraganaString.startswith(curReading):
                if len(result) != 0:
                    raise ValueError("Ambiguous readings")
                result = curReading
                continue

            if not fromLeft and hiraganaString.endswith(curReading):
                if len(result) != 0:
                    raise ValueError("Ambiguous readings")
                result = curReading
                continue
        return result

    def _transliterateWordFromLeft(self, kanjiWord, hiraganaWord, defensively):
        representation = KanjiRepresentation()
        hiraStart = ""
        kanjiRemainder = kanjiWord
        hiraRemainder = hiraganaWord

        while len(kanjiRemainder) > 0 and len(hiraRemainder) > 0:
            if KanaTools.kataToHira(kanjiRemainder) == hiraRemainder:
                representation.addNonKanjiText(kanjiRemainder, True)
                hiraStart = kanjiRemainder = hiraRemainder = ""
                break
            hiraStart, kanjiRemainder, hiraRemainder = self._splitToFirstKanji(kanjiRemainder, hiraRemainder, True)
            representation.addNonKanjiText(hiraStart, True)

            if len(hiraStart) != 0:
                # this block keeps every resolved kanji part, that was followed by equal kana in both kanji and hiragana word.
                try:
                    f, j, k, h = self._transliterateWordFromLeft(kanjiRemainder, hiraRemainder, defensively)
                    return representation.furigana + f, representation.jlab + j, k, h
                except:
                    break

            if len(hiraRemainder) == 0:
                break

            curKanji = kanjiRemainder[0]
            reading = self._getReadingForFirstKanji(curKanji, hiraRemainder, True)
            if len(reading) == 0:
                raise Exception(
                    "No reading found")  # in this case it is likely, that the first deduced readings are wrong, an example is 曳子 (correct:hiki.ko, but is: hi.kiko)

            # kanji remainder length == 1 covers some special cases, where a word ends with an irregular reading. This is safe to use,
            # because if the reading was not unique, an exception would have been raised earlier. It could be, that the error occurred
            # earlier, but this is unlikely.
            if reading == hiraRemainder or (not defensively and len(kanjiRemainder) == 1):
                # reading may not match the entire remainder
                representation.addKanjiText(kanjiRemainder, hiraRemainder, self._learnedKanji, True)
                kanjiRemainder = ""
                hiraRemainder = ""
                break
            else:
                # default case, which is most correct
                representation.addKanjiText(curKanji, reading, self._learnedKanji, True)
                kanjiRemainder = kanjiRemainder[1:]
                hiraRemainder = hiraRemainder[len(reading):]

        return representation.furigana, representation.jlab, kanjiRemainder, hiraRemainder

    def _transliterateWordFromRight(self, kanjiWord, hiraganaWord, defensively):
        representation = KanjiRepresentation()
        hiraStart = ""
        kanjiRemainder = kanjiWord
        hiraRemainder = hiraganaWord

        while len(kanjiRemainder) > 0 and len(hiraRemainder) > 0:
            if KanaTools.kataToHira(kanjiRemainder) == hiraRemainder:
                representation.addNonKanjiText(kanjiRemainder, False)
                hiraStart = kanjiRemainder = hiraRemainder = ""
                break
            hiraStart, kanjiRemainder, hiraRemainder = self._splitToFirstKanji(kanjiRemainder, hiraRemainder, False)
            representation.addNonKanjiText(hiraStart, False)

            if len(hiraStart) != 0:
                # this block keeps every resolved kanji part, that was followed by equal kana in both kanji and hiragana word.
                try:
                    f, j, k, h = self._transliterateWordFromRight(kanjiRemainder, hiraRemainder, defensively)
                    return f + representation.furigana, j + representation.jlab, k, h
                except:
                    break

            if len(hiraRemainder) == 0:
                break

            curKanji = kanjiRemainder[-1]
            reading = ""
            try:
                reading = self._getReadingForFirstKanji(curKanji, hiraRemainder, False)
            except:
                pass

            # in case of an exception (len(reading) == 0), there are the following feasible options:
            # - Assume, that the error occurred in the current kanji. Return the kanji remainder with the kana remainder as reading
            #
            # - Don't know, where the error occurred (could also be an earlier kanji). In this case, return the entire initial kanji word with
            #   the hiragana word as reading. Note, that trailing kana must be removed.

            # Caution: defensive will yield wrong results, if trailing kana is not removed before. This is done by recursive calls to this function.
            if defensively and len(reading) == 0:
                representation.setKanjiText(kanjiWord, hiraganaWord, self._learnedKanji, False)
                kanjiRemainder = ""
                hiraRemainder = ""
                break

            if len(reading) == 0 or reading == hiraRemainder or len(kanjiRemainder) == 1:
                # if no reading from right, use hiragana remainder as furigana for kanji remainder
                representation.addKanjiText(kanjiRemainder, hiraRemainder, self._learnedKanji, False)
                kanjiRemainder = ""
                hiraRemainder = ""
                break

            representation.addKanjiText(curKanji, reading, self._learnedKanji, False)
            kanjiRemainder = kanjiRemainder[:-1]
            hiraRemainder = hiraRemainder[:-len(reading)]

        return representation.furigana, representation.jlab, kanjiRemainder, hiraRemainder

    def _transliterateWord(self, kanjiWord, hiraganaWord, defensively):
        furigana = jlab = kanjiRemainder = hiraRemainder = ""
        try:
            furigana, jlab, kanjiRemainder, hiraRemainder = self._transliterateWordFromLeft(kanjiWord, hiraganaWord, defensively)
        except:
            furigana = jlab = ""
            kanjiRemainder = kanjiWord
            hiraRemainder = hiraganaWord

        if len(kanjiRemainder) == 0 and len(hiraRemainder) > 0:
            raise ValueError("Kanji word reduced, but hiragana chars remaining")

        furiganaRight, jlabRight, kanjiRemainder, hiraRemainder = self._transliterateWordFromRight(kanjiRemainder, hiraRemainder, defensively)

        if len(kanjiRemainder) != 0 or len(hiraRemainder) != 0:
            raise ValueError("Not all characters resolved")

        return furigana + furiganaRight, jlab + jlabRight

#coding: utf8
from Core.KanaTools import *
from Core.KanaRoumajiTransliterator import *
from Core.KanjiKanaTransliterator import *
from Core.ReadingAssistanceType import ReadingAssistanceType
import copy
from Core.Kanjium import *

class ClozePosition:
    def __init__(self, start, length):
        self.start = start
        self.length = length

    def __str__(self):
        return u"(" + str(self.start) + u", " + str(self.length) + u")"

class TextPosition:
    def __init__(self, startWordIndex, endWordIndex, startComplete, endComplete):
        self.startWordIndex = startWordIndex
        self.endWordIndex = endWordIndex
        self.startComplete = startComplete #True: First word selected completely
        self.endComplete = endComplete #True: Last word selected completely

    def __str__(self):
        return u"start word: " + str(self.startWordIndex) + u"\n" \
               + u"end word: " + str(self.endWordIndex) + u"\n" \
               + u"start complete: " + str(self.startComplete) + u"\n" \
               + u"end complete: " + str(self.endComplete) + u"\n" \

class ClozeNotFoundException(Exception):
    def __init__(self, message):
        super(ClozeNotFoundException, self).__init__(message)

#This class is used for accessing words in a japanese sentences
#It is used for:
# - Retrieve a dictionary query for a selected roumaji/hiragana text
# - adding cloze to hiragana/kanji based on selected text
#The transliterator is required in order to enable roumaji as input for dictionary selection (and in the future
#also a mix of kana/roumaji
class JapaneseTextAccess:
    _wordSeparator = u" "

    def __init__(self, spacedHiragana, spacedKanji, hiraganaCloze, kanjiCloze, lemmata, kanaRoumajiTransliterator, kanjiKanaTransliterator, kanjium, defensively):
        assert isinstance(kanaRoumajiTransliterator, KanaRoumajiTransliterator)
        assert isinstance(kanjiKanaTransliterator, KanjiKanaTransliterator)
        assert isinstance(kanjium, Kanjium)
        self._kanaRoumajiTransliterator = kanaRoumajiTransliterator
        self._kanjium = kanjium

        #potential card front sides without clozes
        self._spacedHiragana = spacedHiragana
        self._spacedKanji = spacedKanji
        self._lemmata = lemmata
        self._roumaji = kanaRoumajiTransliterator.kanaToRoumaji(spacedHiragana, "", False, False)
        self._kanaTrainerHiragana = kanaRoumajiTransliterator.kanaToRoumaji(spacedHiragana, "", False, True)
        self._kanaTrainerKatakana = kanaRoumajiTransliterator.kanaToRoumaji(KanaTools.hiraToKata(spacedHiragana), "", False, True)

        # Convert the furigana text to the format produced by text selection within anki (word contains furigana without brackets)
        # This enables word search for full word furigana
        self._furigana, jlab = kanjiKanaTransliterator.transliterateSentence(self._spacedKanji, self._spacedHiragana, defensively, True)
        self._furigana = self._furigana.replace(" ", "").replace(KanjiKanaTransliterator.space, " ").replace(KanjiRepresentation.furiStart, "").replace(KanjiRepresentation.furiEnd, "")
        self._frontTextOptionsNoCloze = [self._spacedHiragana, self._spacedKanji, self._roumaji, self._kanaTrainerHiragana, self._kanaTrainerKatakana, self._lemmata, self._furigana]

        #token / word lists for the front side options
        self._hiraganaToken = spacedHiragana.split()
        self._kanjiToken = spacedKanji.split()
        self._lemmaToken = lemmata.split()

        self._hiraganaCloze = hiraganaCloze
        self._kanjiCloze = kanjiCloze

        self._cleanedClozeDataHira = TextFormatter.replaceClozesWithPlaceholder(hiraganaCloze)
        self._cleanedClozeDataKanji = TextFormatter.replaceClozesWithPlaceholder(kanjiCloze)

        self._kanjiClozeIdentifiers = self.computeKanjiIdentifiers(kanjium)

    def getOriginalHiraganaCloze(self):
        return self._hiraganaCloze

    def getOriginalKanjiCloze(self):
        return self._kanjiCloze

    def getCleanedHiraganaCloze(self):
        return self._cleanedClozeDataHira[0]

    def getCleanedKanjiCloze(self):
        return self._cleanedClozeDataKanji[0]

    def computeKanjiIdentifiers(self, kanjium):
        result = []
        for curWord in self._kanjiToken:
            curIdentifierList = []
            for curChar in KanaTools.kataToHira(curWord): #katakana is processed as hiragana internally
                curReadings = kanjium.getReadings(curChar)
                curReadings.add(curChar) #this is for finding the char itself
                curIdentifierList.append(curReadings)
            result.append(curIdentifierList)
        return result

    def getNewHiraganaCloze(self, hiraganaClozePos, clozeText):
        newClozeIndex = self._getClozeIndex(self._cleanedClozeDataHira[0], hiraganaClozePos)
        allClozeHints = copy.deepcopy(self._cleanedClozeDataHira[1])
        allClozeHints.insert(newClozeIndex, clozeText)
        cleanedClozeWithNewPlaceHolder = self._cleanedClozeDataHira[0][:hiraganaClozePos.start]\
                                         + TextFormatter.clozePlaceholder\
                                         + self._cleanedClozeDataHira[0][hiraganaClozePos.start + hiraganaClozePos.length:]
        return TextFormatter.replacePlaceholdersWithClozes(cleanedClozeWithNewPlaceHolder, allClozeHints)

    def getNewKanjiCloze(self, kanjiClozePos, clozeText):
        newClozeIndex = self._getClozeIndex(self._cleanedClozeDataKanji[0], kanjiClozePos)
        allClozeHints = copy.deepcopy(self._cleanedClozeDataKanji[1])
        allClozeHints.insert(newClozeIndex, clozeText)
        cleanedClozeWithNewPlaceHolder = self._cleanedClozeDataKanji[0][:kanjiClozePos.start]\
                                         + TextFormatter.clozePlaceholder\
                                         + self._cleanedClozeDataKanji[0][kanjiClozePos.start + kanjiClozePos.length:]
        return TextFormatter.replacePlaceholdersWithClozes(cleanedClozeWithNewPlaceHolder, allClozeHints)

    def _getClozeIndex(self, cleanedClozeString, clozePos):
        return cleanedClozeString.count(TextFormatter.clozePlaceholder, 0, clozePos.start) #count all placeholders before new cloze position

    def _getWordIndex(self, selectedText):
        if len(self._kanjiToken) != len(self._lemmaToken) or len(self._kanjiToken) != len(self._hiraganaToken):
            return -1

        #This covers native spelling with kanji; kanji trainer must replace the following section:
        for idx, curKanjiWord in enumerate(self._kanjiToken):
            if curKanjiWord == selectedText:
                return idx

        #This covers mixed kana spelling
        selectedTextHira = self._kanaRoumajiTransliterator.mixedRoumajiToHiragana(selectedText)
        regex = KanaTools.createCaseInsensitiveRegex(selectedTextHira)
        for idx, curHiraganaWord in enumerate(self._hiraganaToken):
            if len(curHiraganaWord) != len(selectedTextHira):
                continue

            match = KanaTools.findPositionCaseInsensitiveRegexInput(regex, curHiraganaWord)
            if len(match) == 1 and match[0][1] == curHiraganaWord:
                return idx

        return -1

    def getHiraganaTextByMixedKana(self, targetString, mixedKanaString):
        mixedKanaStringHiragana = self._kanaRoumajiTransliterator.mixedRoumajiToHiragana(mixedKanaString)
        match = KanaTools.findPositionCaseInsensitiveStringInput(mixedKanaStringHiragana, targetString)
        if len(match) >= 1:
            start = match[0][0]
            length = len(match[0][1])
            return targetString[start : start+length]

        raise ValueError("String not found in hiragana")

    def getHiraganaTextByMixedKanji(self, hiraganaTargetString, mixedKanjiString):
        result = ClozePosition(0, 0)

        searchPattern = u""
        for curChar in mixedKanjiString:
            searchPattern += u"("
            curReadings = self._kanjium.getReadings(curChar)
            for i, curReading in enumerate(curReadings):
                searchPattern += curReading
                if i != len(curReadings)-1 :
                    searchPattern += u"|"
            if len(curReadings) == 0:
                searchPattern += curChar
            searchPattern += u")"

        matchIter = re.search(searchPattern, hiraganaTargetString)
        if matchIter is None:
            raise ClozeNotFoundException("Hiragana cloze indices could not be determined")

        start = matchIter.start()
        length = len(matchIter.group())
        return hiraganaTargetString[start:start+length]

    def findIdentifierInString(self, string, startIdx, identifierSet):
        maxIdx = -1
        for curIdentifier in identifierSet:
            idx = startIdx
            for curChar in curIdentifier:  # try to find current identifier in selected text starting from selTextIdx
                if idx >= len(string) or string[idx] != curChar:
                    idx = startIdx
                    break
                idx += 1

            if idx != startIdx:
                maxIdx = max(maxIdx, idx)
        return maxIdx

    def getKanjiTextByMixedKanji(self, kanjiIdentifiers, kanjiString, mixedKanjiString):
        selTextIdx = 0
        targetIndex = 0
        clozeStart = -1

        if len(kanjiIdentifiers) != len(kanjiString):
            raise ValueError(len(kanjiIdentifiers) != len(kanjiString))

        #-----
        # for idx, curIdentifierSet in enumerate(self._kanjiClozeIdentifiers):
        #     curIdentifierString = u""
        #     for curIdentifier in curIdentifierSet:
        #         curIdentifierString += curIdentifier + u", "
        #
        #     print(str(idx) + u" " + self._cleanedClozeDataKanji[0][idx] + u": " + self._transliterator.kanaToRoumaji(curIdentifierString, u"", False, False))
        #-----

        while True:
            if targetIndex >= len(kanjiIdentifiers):
                raise ValueError("Kanji indices could not be determined")

            curIdentifierSet = kanjiIdentifiers[targetIndex] #set of (multiletter) readings + corresponding kanji OR single other char
            nextSelTextIdx = self.findIdentifierInString(mixedKanjiString, selTextIdx, curIdentifierSet)

            if nextSelTextIdx == -1:
                if clozeStart != -1:
                    targetIndex = clozeStart+1
                else:
                    targetIndex += 1
                selTextIdx = 0
                clozeStart = -1
            else:
                selTextIdx = nextSelTextIdx
                if clozeStart == -1:
                    clozeStart = targetIndex

                targetIndex += 1

                if selTextIdx == len(mixedKanjiString):
                    return kanjiString[clozeStart:targetIndex]

        raise Exception("This should be unreachable")

    def getTextPositionData(self, selectedText):
        for targetText in self._frontTextOptionsNoCloze:
            try:
                index = targetText.index(selectedText)

                leftPart = targetText[:index]
                rightPart = targetText[index + len(selectedText):]

                targetToken = targetText.split(JapaneseTextAccess._wordSeparator)
                sourceToken = selectedText.split(JapaneseTextAccess._wordSeparator)

                startWordIndex = leftPart.count(JapaneseTextAccess._wordSeparator)
                endWordIndex = startWordIndex + selectedText.count(JapaneseTextAccess._wordSeparator)
                startWordComplete = targetToken[startWordIndex] == sourceToken[0] #len(leftPart) == 0 or leftPart.endswith(JapaneseTextAccess._wordSeparator)
                endWordComplete = targetToken[endWordIndex] == sourceToken[-1] #len(rightPart) == 0 or rightPart.startswith(JapaneseTextAccess._wordSeparator)

                return TextPosition(startWordIndex, endWordIndex, startWordComplete, endWordComplete)
            except:
                pass
        raise ValueError(u"selected text not found")

    def checkWordCount(self):
        numWordsHira = self._spacedHiragana.count(JapaneseTextAccess._wordSeparator)
        numWordsSpacedKanji = self._spacedKanji.count(JapaneseTextAccess._wordSeparator)
        numWordsRoumaji = self._roumaji.count(JapaneseTextAccess._wordSeparator)
        numWordsKanaTrainerHira = self._kanaTrainerHiragana.count(JapaneseTextAccess._wordSeparator)
        numWordsKanaTrainerKata = self._kanaTrainerKatakana.count(JapaneseTextAccess._wordSeparator)

        wordCountsEqual = True
        wordCountsEqual &= numWordsHira == numWordsSpacedKanji
        wordCountsEqual &= numWordsHira == numWordsRoumaji
        wordCountsEqual &= numWordsHira == numWordsKanaTrainerHira
        wordCountsEqual &= numWordsHira == numWordsKanaTrainerKata

        if not wordCountsEqual:
            raise Exception(u"Word counts not equal")

    def getStringForFullWord(self, token, startIndex, endIndex):
        if startIndex > endIndex:
            return u""

        result = u""
        for i in range(startIndex, endIndex+1):
            result += token[i] + u" "
        if len(result) == 0:
            raise ValueError(u"Text length == 0")
        return result[:-1] #remove last whitespace

    def getKanaKanjiTextParts(self, searchText, wordIndex):

        selectedTextNoKatakana = KanaTools.kataToHira(searchText)
        hiraganaTargetString = self._hiraganaToken[wordIndex]
        kanjiTargetString = self._kanjiToken[wordIndex]
        kanjiIdentifiers = self._kanjiClozeIdentifiers[wordIndex]

        hiraganaResult = u""
        kanjiResult = u""
        try:
            hiraganaResult = self.getHiraganaTextByMixedKana(hiraganaTargetString, selectedTextNoKatakana)
            kanjiResult = self.getKanjiTextByMixedKanji(kanjiIdentifiers, kanjiTargetString, hiraganaResult)
        except:
            hiraganaResult = self.getHiraganaTextByMixedKanji(hiraganaTargetString, selectedTextNoKatakana)
            kanjiResult = self.getKanjiTextByMixedKanji(kanjiIdentifiers, kanjiTargetString, selectedTextNoKatakana)

        return (hiraganaResult, kanjiResult)

    # This function returns kana, kanji and lemma text fragments retrieved by mapping the selected text to these respective fields.
    # For kana and kanji, this is done by comparing the selected text to the single words of the expression (in different
    # writing systems), which covers 95% of all cases. If word parts are selected, the selected parts are retrieved in the
    # kana / kanji expression by matching of readings. The following cases are possible:
    # - multiple full words selected (easy case)
    # - word part selected (hard case, matching of readings required, which is ambiguous / ill-posed)
    #
    # For word parts, the following cases are possible: start / end / center selected
    # it is currently not checked, if the retrieved string for replacement is in the correct position (start / end / center)
    #
    # The lemma is only returned, if a single full word is selected
    def getTextFragments(self, selectedText):
        selectedText = selectedText.replace(KanjiKanaTransliterator.space, " ") # enables furigana as input text
        self.checkWordCount()

        selectedText = selectedText.strip()
        selectedTextToken = selectedText.split(u" ")
        textPositionData = self.getTextPositionData(selectedText)

        hiraganaText = kanjiText = lemmaText = u""
        if textPositionData.startComplete and textPositionData.endComplete:
            hiraganaText = self.getStringForFullWord(self._hiraganaToken, textPositionData.startWordIndex, textPositionData.endWordIndex)
            kanjiText = self.getStringForFullWord(self._kanjiToken, textPositionData.startWordIndex, textPositionData.endWordIndex)
            try:
                lemmaText = self.getStringForFullWord(self._lemmaToken, textPositionData.startWordIndex, textPositionData.endWordIndex)
            except:
                pass
        else:
            if not textPositionData.startComplete:
                kanaKanjiTextParts = self.getKanaKanjiTextParts(selectedTextToken[0], textPositionData.startWordIndex)
                hiraganaText += kanaKanjiTextParts[0]
                kanjiText += kanaKanjiTextParts[1]

            if textPositionData.startWordIndex != textPositionData.endWordIndex:
                hiraganaText += JapaneseTextAccess._wordSeparator
                kanjiText += JapaneseTextAccess._wordSeparator

            startIdx = textPositionData.startWordIndex
            if not textPositionData.startComplete:
                startIdx+=1

            endIdx = textPositionData.endWordIndex
            if not textPositionData.endComplete:
                endIdx-=1

            hiraganaText += self.getStringForFullWord(self._hiraganaToken, startIdx, endIdx)
            kanjiText += self.getStringForFullWord(self._kanjiToken, startIdx, endIdx)

            if textPositionData.startWordIndex != textPositionData.endWordIndex and not textPositionData.endComplete:
                if len(hiraganaText) != 0 and hiraganaText[-1] != JapaneseTextAccess._wordSeparator:
                    hiraganaText += JapaneseTextAccess._wordSeparator
                    kanjiText += JapaneseTextAccess._wordSeparator

                kanaKanjiTextParts = self.getKanaKanjiTextParts(selectedTextToken[-1], textPositionData.endWordIndex)
                hiraganaText += kanaKanjiTextParts[0]
                kanjiText += kanaKanjiTextParts[1]
        return (hiraganaText, kanjiText, lemmaText)

    # tries mapping the selected text to the desired reading assistance type. Note that this function is tailored
    # for getting good context menu items (i.e. latin input for jgram or kanji input for google translate)
    def tryMapTo(self, selectedText, readingAssistanceType):
        result = selectedText

        try:
            textPositionData = self.getTextPositionData(selectedText)
            fullWords = textPositionData.startComplete and textPositionData.endComplete

            if readingAssistanceType == ReadingAssistanceType.latin:
                if fullWords:
                    result = self.getStringForFullWord(self._roumaji.split(JapaneseTextAccess._wordSeparator), textPositionData.startWordIndex, textPositionData.endWordIndex)
                else:
                    result = self._kanaRoumajiTransliterator.kanaToRoumaji(selectedText, "", False, False)
            elif readingAssistanceType == ReadingAssistanceType.none:
                if not fullWords:
                    raise Exception
                result = self.getStringForFullWord(self._kanjiToken, textPositionData.startWordIndex, textPositionData.endWordIndex)
        except:
            pass

        return result.strip()


    def getClozePositions(self, selectedText):
        textFragments = self.getTextFragments(selectedText)

        hiraganaStartIndex = self._cleanedClozeDataHira[0].find(textFragments[0])
        if hiraganaStartIndex == -1:
            raise ClozeNotFoundException(u"Hiragana cloze position not found")

        kanjiStartIndex  = self._cleanedClozeDataKanji[0].find(textFragments[1])
        if kanjiStartIndex == -1:
            raise ClozeNotFoundException(u"Kanji cloze position not found")

        hiraganaClozePos = ClozePosition(hiraganaStartIndex, len(textFragments[0]))
        kanjiClozePos = ClozePosition(kanjiStartIndex, len(textFragments[1]))
        return (hiraganaClozePos, kanjiClozePos)

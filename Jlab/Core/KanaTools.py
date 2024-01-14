#coding: utf8
# unicode blocks: http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
import re

class KanaType:
    hiragana = "Hiragana"
    katakana = "Katakana"

class KanaTools:
    upperLowerRegexCreator = [
        u"[あぁ]",
        u"[いぃ]",
        u"[うぅ]",
        u"[えぇ]",
        u"[おぉ]",
        u"[かゕ]",
        u"[けゖ]",
        u"[わゎ]"
    ]

    geminationLikely = {
        u"か",
        u"き",
        u"く",
        u"け",
        u"こ",
        u"つ",
        u"ち"
    }

    dakuten = {
        u"か": [u"が"],
        u"き": [u"ぎ"],
        u"く": [u"ぐ"],
        u"け": [u"げ"],
        u"こ": [u"ご"],
        u"さ": [u"ざ"],
        u"し": [u"じ"],
        u"す": [u"ず"],
        u"せ": [u"ぜ"],
        u"そ": [u"ぞ"],
        u"た": [u"だ"],
        u"ち": [u"ぢ"],
        u"つ": [u"づ"],
        u"て": [u"で"],
        u"と": [u"ど"],
        u"は": [u"ば", u"ぱ"],
        u"ひ": [u"び", u"ぴ"],
        u"ふ": [u"ぶ", u"ぷ"],
        u"へ": [u"べ", u"ぺ"],
        u"ほ": [u"ぼ", u"ぽ"]
    }

    #init hiragana <-> katakana conversion dictionaries
    _kataToHira = {}
    _hiraToKata = {}

    kataStart = 0x30A1
    kataEnd = 0x30F6
    hiraStart = 0x3041
    for i in range(0, kataEnd - kataStart):
        _kataToHira[chr(kataStart + i)] = chr(hiraStart + i)
        _hiraToKata[chr(hiraStart + i)] = chr(kataStart + i)

    #init regex for checking non-katakana characters
    _rxNoKatakana = re.compile(u"[^ァ-ー]")
    rxKana = re.compile("[\u3040-\u30ff]")

    # string is katakana, if no other char type is found. Note, that whitespaces and other chars will return false.
    @staticmethod
    def isKatakana(inputData):
        return not KanaTools._rxNoKatakana.search(inputData)

    #Converts every hiragana character in the input string to katakana (non-hiragana is adopted unchanged)
    @staticmethod
    def hiraToKata(stringWithHiragana):
        result = ""
        for curChar in stringWithHiragana:
            convertedChar = KanaTools._hiraToKata.get(curChar, 0)
            if convertedChar != 0:
                result += convertedChar
            else:
                result += curChar
        return result


    #Converts every katakana character in the input string to hiragana (non-katakana is adopted unchanged)
    @staticmethod
    def kataToHira(stringWithKatakana):
        result = ""
        for curChar in stringWithKatakana:
            convertedChar = KanaTools._kataToHira.get(curChar, 0)
            if convertedChar != 0:
                result += convertedChar
            else:
                result += curChar
        return result

    @staticmethod
    #Creates a regular expression for a kana string with wrong capitalization. The regex allows to find all occurences
    #of the wronly capitalized string within a given other kana string that is spelled correctly.
    def createCaseInsensitiveRegex(kanaStringWrongCase):
        caseInsensitiveRegexCreator = kanaStringWrongCase
        for curChars in KanaTools.upperLowerRegexCreator:
            caseInsensitiveRegexCreator = re.sub(curChars, curChars, caseInsensitiveRegexCreator)

        return re.compile(caseInsensitiveRegexCreator)

    @staticmethod
    #Returns all (correctly spelled) occurences of a wrongly capitalized kana string within a correctly spelled string.
    #The wrongly spelled kana string is represented as regex. This allows to find one wrongly spelled input string within
    #multiple others without having to recompile the regex.
    def findPositionCaseInsensitiveRegexInput(kanaRegexCaseInsensitive, kanaStringCorrectCase):
        #each element of finditer is a MatchObject. start() returns the index of the complete match, group() the entire match
        matchResult = kanaRegexCaseInsensitive.finditer(kanaStringCorrectCase)
        result = []
        for curMatch in matchResult:
            result.append((curMatch.start(), curMatch.group()))
        return result

    @staticmethod
    #finds all occurences of a wrongly capitalized kana string within a correctly spelled kana string. Convenience
    #function that takes two strings as input
    def findPositionCaseInsensitiveStringInput(kanaStringWrongCase, kanaStringCorrectCase):
        caseInsensitiveRegex = KanaTools.createCaseInsensitiveRegex(kanaStringWrongCase)
        return KanaTools.findPositionCaseInsensitiveRegexInput(caseInsensitiveRegex, kanaStringCorrectCase)

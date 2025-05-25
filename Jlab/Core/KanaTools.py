# coding: utf8
# unicode blocks: http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
import re


class KanaType:
    hiragana = "Hiragana"
    katakana = "Katakana"


class KanaTools:
    upperLowerRegexCreator = ["[あぁ]", "[いぃ]", "[うぅ]", "[えぇ]", "[おぉ]", "[かゕ]", "[けゖ]", "[わゎ]"]

    geminationLikely = {"か", "き", "く", "け", "こ", "つ", "ち"}

    dakuten = {
        "か": ["が"],
        "き": ["ぎ"],
        "く": ["ぐ"],
        "け": ["げ"],
        "こ": ["ご"],
        "さ": ["ざ"],
        "し": ["じ"],
        "す": ["ず"],
        "せ": ["ぜ"],
        "そ": ["ぞ"],
        "た": ["だ"],
        "ち": ["ぢ"],
        "つ": ["づ"],
        "て": ["で"],
        "と": ["ど"],
        "は": ["ば", "ぱ"],
        "ひ": ["び", "ぴ"],
        "ふ": ["ぶ", "ぷ"],
        "へ": ["べ", "ぺ"],
        "ほ": ["ぼ", "ぽ"],
    }

    # init hiragana <-> katakana conversion dictionaries
    _kataToHira = {}
    _hiraToKata = {}

    kataStart = 0x30A1
    kataEnd = 0x30F6
    hiraStart = 0x3041
    for i in range(0, kataEnd - kataStart):
        _kataToHira[chr(kataStart + i)] = chr(hiraStart + i)
        _hiraToKata[chr(hiraStart + i)] = chr(kataStart + i)

    # init regex for checking non-katakana characters
    _rxNoKatakana = re.compile("[^ァ-ー]")
    rxKana = re.compile("[\u3040-\u30ff]")

    # string is katakana, if no other char type is found. Note, that whitespaces and other chars will return false.
    @staticmethod
    def isKatakana(inputData):
        return not KanaTools._rxNoKatakana.search(inputData)

    # Converts every hiragana character in the input string to katakana (non-hiragana is adopted unchanged)
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

    # Converts every katakana character in the input string to hiragana (non-katakana is adopted unchanged)
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
    # Creates a regular expression for a kana string with wrong capitalization. The regex allows to find all occurences
    # of the wronly capitalized string within a given other kana string that is spelled correctly.
    def createCaseInsensitiveRegex(kanaStringWrongCase):
        caseInsensitiveRegexCreator = kanaStringWrongCase
        for curChars in KanaTools.upperLowerRegexCreator:
            caseInsensitiveRegexCreator = re.sub(curChars, curChars, caseInsensitiveRegexCreator)

        return re.compile(caseInsensitiveRegexCreator)

    @staticmethod
    # Returns all (correctly spelled) occurences of a wrongly capitalized kana string within a correctly spelled string.
    # The wrongly spelled kana string is represented as regex. This allows to find one wrongly spelled input string within
    # multiple others without having to recompile the regex.
    def findPositionCaseInsensitiveRegexInput(kanaRegexCaseInsensitive, kanaStringCorrectCase):
        # each element of finditer is a MatchObject. start() returns the index of the complete match, group() the entire match
        matchResult = kanaRegexCaseInsensitive.finditer(kanaStringCorrectCase)
        result = []
        for curMatch in matchResult:
            result.append((curMatch.start(), curMatch.group()))
        return result

    @staticmethod
    # finds all occurences of a wrongly capitalized kana string within a correctly spelled kana string. Convenience
    # function that takes two strings as input
    def findPositionCaseInsensitiveStringInput(kanaStringWrongCase, kanaStringCorrectCase):
        caseInsensitiveRegex = KanaTools.createCaseInsensitiveRegex(kanaStringWrongCase)
        return KanaTools.findPositionCaseInsensitiveRegexInput(caseInsensitiveRegex, kanaStringCorrectCase)

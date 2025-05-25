# coding: utf8
import sqlite3
import os.path
import re
from Core.KanaTools import *
from Core.KanjiTools import *


class Kanjium:
    readingCleanupRegex = re.compile("\s|（(.*?)）|\((.*?)\)")  # matches whitespaces and anything in brackets

    def __init__(self, path=""):
        if len(path) == 0:
            path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/Data/kanjidb.sqlite"
        if not os.path.isfile(path):
            raise Exception("Invalid path: " + path)
        self._db = sqlite3.connect(path, check_same_thread=False)

    def close(self):
        self._db.close()

    # Returns all readings of the kanji in hiragana without okurigana
    def getReadings(self, kanji):
        cursor = self._db.cursor()
        cursor.execute("select onyomi, kunyomi, nanori " "from kanjidict " "where kanji = ?", [kanji])

        rows = cursor.fetchall()
        result = set()
        for row in rows:
            if row[0] is not None:
                for curOnyomi in Kanjium.readingCleanupRegex.sub("", row[0]).split("、"):
                    if len(curOnyomi) != 0:
                        result.add(KanaTools.kataToHira(curOnyomi))
            if row[1] is not None:
                for curKunyomi in Kanjium.readingCleanupRegex.sub("", row[1]).split("、"):
                    if len(curKunyomi) != 0:
                        result.add(curKunyomi)
            if row[2] is not None:
                for nanori in Kanjium.readingCleanupRegex.sub("", row[2]).split("、"):
                    if len(nanori) != 0:
                        result.add(nanori)

        modifiedReadings = self._getModifiedReadings(result)
        result.update(modifiedReadings)

        modifiedReadings = self._getModifiedReadingsGemination(result)
        result.update(modifiedReadings)
        return result
        if kanji == "一":
            result.add("いっ")
        return result

    def countReadings(self):
        cursor = self._db.cursor()
        cursor.execute("select kanji, onyomi, kunyomi " "from kanjidict ")
        rows = cursor.fetchall()

        readings = ""
        for row in rows:
            if row[1] is not None:
                readings += row[1] + "、"
            if row[2] is not None:
                readings += row[2] + "、"
        print("Total readings: " + str(readings.count("、")))

        heisigSet = set(KanjiTools.heisigList)
        readings = ""
        for row in rows:
            if row[0] not in heisigSet:
                continue
            if row[1] is not None:
                readings += row[1] + "、"
            if row[2] is not None:
                readings += row[2] + "、"
        print("Heisig readings: " + str(readings.count("、")))

    def _getModifiedReadings(self, readings):
        modifiedReadings = set()
        for curReading in readings:
            dakuten = KanaTools.dakuten.get(curReading[0], 0)
            if dakuten != 0:
                right = curReading[1:]
                for curChar in dakuten:
                    modifiedReadings.add(curChar + right)
        return modifiedReadings

    def _getModifiedReadingsGemination(self, readings):
        modifiedReadings = set()
        for curReading in readings:
            if curReading[-1] in KanaTools.geminationLikely:
                if len(curReading) == 1:
                    modifiedReadings.add(curReading + "っ")
                else:
                    modifiedReadings.add(curReading[:-1] + "っ")
        return modifiedReadings

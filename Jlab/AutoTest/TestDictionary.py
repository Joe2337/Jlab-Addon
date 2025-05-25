# coding: utf8

import unittest
from Dict.JapaneseDictionary import JapaneseDictionary


class TestDictionary(unittest.TestCase):

    # Ensures, that the result of the dictionary search has a given format. If the format is changed, the cloze editor
    # must be adapted (ClozeEditor.getLookedUpReadings / Expression must not be missed)
    def testDictionarySearchResult(self):
        dict = JapaneseDictionary()
        firstHit = dict.lookup("起す")[0]
        self.assertEqual(firstHit[0], "起こす, 起す")
        self.assertEqual(firstHit[1], "おこす")
        self.assertEqual(firstHit[4], "to raise; to raise up; to set up; to pick up")

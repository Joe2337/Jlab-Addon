#coding: utf8

import unittest
from Core.KanaTrainerData import *

class TestKanaTrainer(unittest.TestCase):

    def testKanaDisplayType(self):
        data = KanaTrainerData()
        data.kanaType = KanaType.hiragana
        data.showOppositeKana = False
        data.oppositeKanaStepSize = 3

        for index in range(2, 3):
            if(data.getKanaTypeForDisplay(index) != KanaType.hiragana):
                raise Exception(u"Wrong kana type for display")

        data.showOppositeKana = True
        if(data.getKanaTypeForDisplay(2) != KanaType.hiragana):
            raise Exception(u"Wrong kana type for display")
        if(data.getKanaTypeForDisplay(3) != KanaType.katakana):
            raise Exception(u"Wrong kana type for display")
        if(data.getKanaTypeForDisplay(4) != KanaType.hiragana):
            raise Exception(u"Wrong kana type for display")

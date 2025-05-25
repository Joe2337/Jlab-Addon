# coding: utf8

import unittest
from Core.Settings import *


class TestSettings(unittest.TestCase):

    def testCardFormatChanged(self):
        settingsA = Settings()
        settingsB = Settings()

        if settingsA.cardFormatChanged(settingsB):
            raise Exception("Card format changed")

        settingsB.listeningBackReadingAssistance = "a"
        if not settingsA.cardFormatChanged(settingsB):
            raise Exception("Card format not changed ")

        settingsB = Settings()
        settingsB.listeningFrontReadingAssistance = "a"
        if not settingsA.cardFormatChanged(settingsB):
            raise Exception("Card format not changed ")

        settingsB = Settings()
        settingsB.clozeFrontReadingAssistance = "a"
        if not settingsA.cardFormatChanged(settingsB):
            raise Exception("Card format not changed ")

        settingsB = Settings()
        settingsB.clozeBackReadingAssistance = "a"
        if not settingsA.cardFormatChanged(settingsB):
            raise Exception("Card format not changed ")

        settingsB = Settings()
        settingsB.clozeEditorReadingAssistance = "a"
        if settingsA.cardFormatChanged(settingsB):
            raise Exception("Card format not changed ")

    # test, if current version can be saved and loaded
    def testIStorable(self):
        settingsA = Settings()
        settingsA.fromDictionary(settingsA.toDictionary())

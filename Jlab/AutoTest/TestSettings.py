#coding: utf8

import unittest
from Core.Settings import *

class TestSettings(unittest.TestCase):

    def testCardFormatChanged(self):
        settingsA = Settings()
        settingsB = Settings()

        if settingsA.cardFormatChanged(settingsB):
            raise Exception(u"Card format changed")

        settingsB.listeningBackReadingAssistance = u"a"
        if not settingsA.cardFormatChanged(settingsB):
            raise Exception(u"Card format not changed ")

        settingsB = Settings()
        settingsB.listeningFrontReadingAssistance = u"a"
        if not settingsA.cardFormatChanged(settingsB):
            raise Exception(u"Card format not changed ")

        settingsB = Settings()
        settingsB.clozeFrontReadingAssistance = u"a"
        if not settingsA.cardFormatChanged(settingsB):
            raise Exception(u"Card format not changed ")

        settingsB = Settings()
        settingsB.clozeBackReadingAssistance = u"a"
        if not settingsA.cardFormatChanged(settingsB):
            raise Exception(u"Card format not changed ")

        settingsB = Settings()
        settingsB.clozeEditorReadingAssistance = u"a"
        if settingsA.cardFormatChanged(settingsB):
            raise Exception(u"Card format not changed ")

    #test, if current version can be saved and loaded
    def testIStorable(self):
        settingsA = Settings()
        settingsA.fromDictionary(settingsA.toDictionary())

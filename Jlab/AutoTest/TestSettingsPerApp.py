#coding: utf8

import unittest
from Core.SettingsPerApp import *
import tempfile
import codecs

class TestSettings(unittest.TestCase):

    def testFolderChangedTargetEmpty(self):
        settingsPerApp = SettingsPerApp()
        sourceDir = tempfile.mkdtemp()
        targetDir = tempfile.mkdtemp()

        settingsPerApp.dataFolder = sourceDir

        with codecs.open(sourceDir + u"/settings.txt", u"w", encoding=u"utf-8") as file:
            file.close()

        settingsPerApp.setDataFolder(targetDir)
        if not os.path.exists(targetDir + u"/settings.txt"):
            raise Exception(u"Settings not copied")

        shutil.rmtree(sourceDir)
        shutil.rmtree(targetDir)

    def testFolderChangedTargetNotEmpty(self):
        settingsPerApp = SettingsPerApp()
        sourceDir = tempfile.mkdtemp()
        targetDir = tempfile.mkdtemp()

        settingsPerApp.dataFolder = sourceDir

        with codecs.open(sourceDir + u"/settings.txt", u"w", encoding=u"utf-8") as file:
            file.close()

        with codecs.open(targetDir + u"/settings.txt", u"w", encoding=u"utf-8") as file:
            file.write(u"A")
            file.close()

        settingsPerApp.setDataFolder(targetDir)
        with codecs.open(targetDir + u"/settings.txt", "r", encoding="utf-8") as file:
            content = file.read()
            file.close()
            if content != u"A":
                raise Exception(u"Settings overwritten")

        shutil.rmtree(sourceDir)
        shutil.rmtree(targetDir)

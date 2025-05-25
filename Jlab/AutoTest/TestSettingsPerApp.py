# coding: utf8

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

        with codecs.open(sourceDir + "/settings.txt", "w", encoding="utf-8") as file:
            file.close()

        settingsPerApp.setDataFolder(targetDir)
        if not os.path.exists(targetDir + "/settings.txt"):
            raise Exception("Settings not copied")

        shutil.rmtree(sourceDir)
        shutil.rmtree(targetDir)

    def testFolderChangedTargetNotEmpty(self):
        settingsPerApp = SettingsPerApp()
        sourceDir = tempfile.mkdtemp()
        targetDir = tempfile.mkdtemp()

        settingsPerApp.dataFolder = sourceDir

        with codecs.open(sourceDir + "/settings.txt", "w", encoding="utf-8") as file:
            file.close()

        with codecs.open(targetDir + "/settings.txt", "w", encoding="utf-8") as file:
            file.write("A")
            file.close()

        settingsPerApp.setDataFolder(targetDir)
        with codecs.open(targetDir + "/settings.txt", "r", encoding="utf-8") as file:
            content = file.read()
            file.close()
            if content != "A":
                raise Exception("Settings overwritten")

        shutil.rmtree(sourceDir)
        shutil.rmtree(targetDir)

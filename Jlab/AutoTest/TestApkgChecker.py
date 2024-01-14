#coding: utf8

import unittest
import os
from AnkiTools.ApkgChecker import ApkgChecker

class TestApkgChecker(unittest.TestCase):

    def testApkgChecker(self):
        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + u"/Misc/jlab-testdeck.apkg"
        self.assertEqual(ApkgChecker.isJlabApkg(path), True)

        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + u"/Misc/non-jlab-testdeckあある.apkg"
        self.assertEqual(ApkgChecker.isJlabApkg(path), False)

#coding: utf8

import unittest
from Core.HiddenSettings import *
from Persistence.FileStorageEngine import *
import os
import importlib

fileStorageEngine = FileStorageEngine()

def testClass(unitTest, moduleName, className):
    module = importlib.import_module(moduleName)
    class_ = getattr(module, className)
    currentVersion = class_().getVersion()
    for oldVersion in range(0, currentVersion):
        oldVersionFileName = className + "V" + str(oldVersion).zfill(3)
        print("testing " + oldVersionFileName + "\n")
        curSettings = class_()
        unitTest.assertTrue(fileStorageEngine.fileOutdated(FileStorageEngine.makePath(TestSerialization.oldFileFolder, oldVersionFileName), curSettings))
        fileStorageEngine.load(curSettings, TestSerialization.oldFileFolder, oldVersionFileName)

class TestSerialization(unittest.TestCase):
    oldFileFolder = os.path.dirname(__file__) + "/OldFileVersions"

    def testOutdated(self):
        # same version
        d0 = {
            "version" : 0
        }

        d1 = {
            "version" : 0
        }
        self.assertFalse(fileStorageEngine._dict0Outdated(d0, d1))



        # 1 is newer
        d0 = {
            "version" : 0
        }

        d1 = {
            "version" : 1
        }
        self.assertTrue(fileStorageEngine._dict0Outdated(d0, d1))



        # 0 is newer
        d0 = {
            "version" : 1
        }

        d1 = {
            "version" : 0
        }
        self.assertRaises(Exception, fileStorageEngine._dict0Outdated, d0, d1)



        # nested; outer have equal version, 1 is newer by inner dictionary
        d0 = {
            "version" : 0,
            "otherDict" : {
                "version" : 0
            }
        }

        d1 = {
            "version" : 0,
            "otherDict" : {
                "version" : 1
            }
        }
        self.assertTrue(fileStorageEngine._dict0Outdated(d0, d1))



    def testSerializedClasses(self):
        testClass(self, "Core.HiddenSettings", "HiddenSettings")

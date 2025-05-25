from Core.CurrentVersion import CurrentVersion
from Core.UpdateInformation import UpdateInformation
from distutils.dir_util import copy_tree
import glob
import os
import shutil
import sys

deploymentFolder = "C:/Tmp/AnkiAddon" + UpdateInformation.makeVersionString(CurrentVersion.currentVersionMajor, CurrentVersion.currentVersionMinor) + "/"

if len(sys.argv) == 2:
    deploymentFolder = sys.argv[1]

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)


def copyAllPyFiles(sourceFolder, targetFolder):
    files = glob.iglob(os.path.join(sourceFolder, "*.py"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, targetFolder)


def deploySubFolder(subFolder):
    curTargetFolder = deploymentFolder + subFolder
    curSourceFolder = os.path.dirname(__file__) + "/Jlab/" + subFolder
    if not os.path.isdir(curTargetFolder):
        os.makedirs(curTargetFolder)
    copyAllPyFiles(curSourceFolder, curTargetFolder)


deploySubFolder("AnkiTools/")
deploySubFolder("Core/")
deploySubFolder("Dict/")
deploySubFolder("Global/")
deploySubFolder("Persistence/")
copyAllPyFiles(os.path.dirname(__file__) + "/Jlab", deploymentFolder)
shutil.copy2(os.path.dirname(__file__) + "/changelog.txt", deploymentFolder)

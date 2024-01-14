from Core.CurrentVersion import CurrentVersion
from Core.UpdateInformation import UpdateInformation
from distutils.dir_util import copy_tree
import glob
import os
import shutil
import sys

deploymentFolder = u"C:/Tmp/AnkiAddon" + UpdateInformation.makeVersionString(CurrentVersion.currentVersionMajor, CurrentVersion.currentVersionMinor) + u"/"

if len(sys.argv) == 2:
    deploymentFolder = sys.argv[1]

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

def copyAllPyFiles(sourceFolder, targetFolder):
    files = glob.iglob(os.path.join(sourceFolder, u"*.py"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, targetFolder)

def deploySubFolder(subFolder):
    curTargetFolder = deploymentFolder + subFolder
    curSourceFolder = os.path.dirname(__file__) + "/Jlab/" + subFolder
    if not os.path.isdir(curTargetFolder):
        os.makedirs(curTargetFolder)
    copyAllPyFiles(curSourceFolder, curTargetFolder)

deploySubFolder(u"AnkiTools/")
deploySubFolder(u"Core/")
deploySubFolder(u"Dict/")
deploySubFolder(u"Global/")
deploySubFolder(u"Persistence/")
copyAllPyFiles(os.path.dirname(__file__) + u"/Jlab", deploymentFolder)
shutil.copy2(os.path.dirname(__file__) + "/changelog.txt", deploymentFolder)
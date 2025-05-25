from Persistence.IStorable import *


class UpdateInformation(IStorable):
    def __init__(self):
        self.version = 0
        self.addonVersion = "0.0"
        self.updateUrl = ""
        self.testOnly = False

    @staticmethod
    def makeVersionString(major, minor):
        return str(major) + "." + str(minor)

    def getMajorMinor(self):
        versions = self.addonVersion.split(".")
        if len(versions) != 2:
            raise ValueError("Wrong version string")
        return (int(versions[0]), int(versions[1]))

    def toDictionary(self):
        return {
            "version": self.getVersion(),
            "identifier": self.getIdentifier(),
            "addonVersion": self.addonVersion,
            "updateUrl": self.updateUrl,
            "testOnly": self.testOnly,
        }

    def fromDictionary(self, dictionary):
        version = dictionary["version"]
        self.addonVersion = dictionary["addonVersion"]
        self.updateUrl = dictionary["updateUrl"]
        self.testOnly = dictionary["testOnly"]

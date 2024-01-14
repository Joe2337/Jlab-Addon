from Persistence.IStorable import *

class UpdateInformation(IStorable):
    def __init__(self):
        self.version = 0
        self.addonVersion = u"0.0"
        self.updateUrl = u""
        self.testOnly = False

    @staticmethod
    def makeVersionString(major, minor):
        return str(major) + u"." + str(minor)

    def getMajorMinor(self):
        versions = self.addonVersion.split(u".")
        if len(versions) != 2:
            raise ValueError(u"Wrong version string")
        return (int(versions[0]), int(versions[1]))

    def toDictionary(self):
        return {
            u"version": self.getVersion(),
            u"identifier": self.getIdentifier(),
            u"addonVersion": self.addonVersion,
            u"updateUrl": self.updateUrl,
            u"testOnly": self.testOnly
        }

    def fromDictionary(self, dictionary):
        version = dictionary[u"version"]
        self.addonVersion = dictionary[u"addonVersion"]
        self.updateUrl = dictionary[u"updateUrl"]
        self.testOnly = dictionary[u"testOnly"]

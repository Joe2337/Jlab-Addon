from Persistence.IStorable import *
from Core.ReadingAssistanceType import *

class Settings(IStorable):
    def __init__(self):
        self.version = 1
        self.listeningFrontReadingAssistance = ReadingAssistanceType.latin
        self.listeningBackReadingAssistance = ReadingAssistanceType.latin
        self.clozeFrontReadingAssistance = ReadingAssistanceType.latin
        self.clozeBackReadingAssistance = ReadingAssistanceType.latin
        self.clozeEditorReadingAssistance = ReadingAssistanceType.latin

        self.manageJlabCards = False
        self.promptBeforeCardManagementAction = True
        self.endAction = "Tag"
        self.lcEndInterval = 14
        self.clozeEndInterval = 14

    def toDictionary(self):
        return {
            u"version" : self.getVersion(),
            u"identifier" : self.getIdentifier(),
            u"listeningFrontReadingAssistance" : self.listeningFrontReadingAssistance,
            u"listeningBackReadingAssistance" : self.listeningBackReadingAssistance,
            u"clozeFrontReadingAssistance" : self.clozeFrontReadingAssistance,
            u"clozeBackReadingAssistance" : self.clozeBackReadingAssistance,
            u"clozeEditorReadingAssistance" : self.clozeEditorReadingAssistance,
            u"manageJlabCards" : self.manageJlabCards,
            u"promptBeforeCardManagementAction" : self.promptBeforeCardManagementAction,
            u"endAction" : self.endAction,
            u"lcEndInterval" : self.lcEndInterval,
            u"clozeEndInterval" : self.clozeEndInterval
        }

    def fromDictionary(self, dictionary):
        version = dictionary[u"version"]
        self.listeningFrontReadingAssistance = dictionary[u"listeningFrontReadingAssistance"]
        self.listeningBackReadingAssistance = dictionary[u"listeningBackReadingAssistance"]
        self.clozeFrontReadingAssistance = dictionary[u"clozeFrontReadingAssistance"]
        self.clozeBackReadingAssistance = dictionary[u"clozeBackReadingAssistance"]
        self.clozeEditorReadingAssistance = dictionary[u"clozeEditorReadingAssistance"]

        if version == 0:
            self.manageJlabCards = True #version 0's cards are always managed

        if version >= 1:
            self.manageJlabCards = dictionary[u"manageJlabCards"]
            self.promptBeforeCardManagementAction = dictionary[u"promptBeforeCardManagementAction"]
            self.endAction = dictionary[u"endAction"]
            self.lcEndInterval = dictionary[u"lcEndInterval"]
            self.clozeEndInterval = dictionary[u"clozeEndInterval"]

    def cardFormatChanged(self, settings):
        return self.listeningFrontReadingAssistance != settings.listeningFrontReadingAssistance or \
               self.listeningBackReadingAssistance != settings.listeningBackReadingAssistance or \
               self.clozeFrontReadingAssistance != settings.clozeFrontReadingAssistance or \
               self.clozeBackReadingAssistance != settings.clozeBackReadingAssistance
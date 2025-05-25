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
            "version": self.getVersion(),
            "identifier": self.getIdentifier(),
            "listeningFrontReadingAssistance": self.listeningFrontReadingAssistance,
            "listeningBackReadingAssistance": self.listeningBackReadingAssistance,
            "clozeFrontReadingAssistance": self.clozeFrontReadingAssistance,
            "clozeBackReadingAssistance": self.clozeBackReadingAssistance,
            "clozeEditorReadingAssistance": self.clozeEditorReadingAssistance,
            "manageJlabCards": self.manageJlabCards,
            "promptBeforeCardManagementAction": self.promptBeforeCardManagementAction,
            "endAction": self.endAction,
            "lcEndInterval": self.lcEndInterval,
            "clozeEndInterval": self.clozeEndInterval,
        }

    def fromDictionary(self, dictionary):
        version = dictionary["version"]
        self.listeningFrontReadingAssistance = dictionary["listeningFrontReadingAssistance"]
        self.listeningBackReadingAssistance = dictionary["listeningBackReadingAssistance"]
        self.clozeFrontReadingAssistance = dictionary["clozeFrontReadingAssistance"]
        self.clozeBackReadingAssistance = dictionary["clozeBackReadingAssistance"]
        self.clozeEditorReadingAssistance = dictionary["clozeEditorReadingAssistance"]

        if version == 0:
            self.manageJlabCards = True  # version 0's cards are always managed

        if version >= 1:
            self.manageJlabCards = dictionary["manageJlabCards"]
            self.promptBeforeCardManagementAction = dictionary["promptBeforeCardManagementAction"]
            self.endAction = dictionary["endAction"]
            self.lcEndInterval = dictionary["lcEndInterval"]
            self.clozeEndInterval = dictionary["clozeEndInterval"]

    def cardFormatChanged(self, settings):
        return (
            self.listeningFrontReadingAssistance != settings.listeningFrontReadingAssistance
            or self.listeningBackReadingAssistance != settings.listeningBackReadingAssistance
            or self.clozeFrontReadingAssistance != settings.clozeFrontReadingAssistance
            or self.clozeBackReadingAssistance != settings.clozeBackReadingAssistance
        )

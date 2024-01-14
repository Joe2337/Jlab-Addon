from aqt import mw
from anki.lang import _
from AnkiTools.TemplateNames import TemplateNames
from AnkiTools.CardSearch import *
from aqt.utils import showInfo

class JlabOptions:

    @staticmethod
    def addDefaultConfigurations():
        if not JlabOptions.hasListeningConfig():
            mw.col.decks.add_config(JlabOptions.listeningConfigName, JlabOptions.listeningConfig)
        if not JlabOptions.hasClozeConfig():
            mw.col.decks.add_config(JlabOptions.clozeConfigName, JlabOptions.clozeConfig)
        if not JlabOptions.hasBeginnerParentConfig():
            mw.col.decks.add_config(JlabOptions.parentConfigName, JlabOptions.parentConfig)

    @staticmethod
    def setOptionsForNewDecks(newDeckNameList):
        lConf = JlabOptions.getListeningConfigId()
        cConf = JlabOptions.getClozeConfigId()
        pConf = JlabOptions.getParentConfigId()

        newDeckNameSet = set(newDeckNameList)
        for curDeck in mw.col.decks.decks.values():
            curDeckName = curDeck[u"name"]

            if curDeckName == _("Default") or curDeckName not in newDeckNameSet:
                continue

            clozeQuery = u"\"deck:" + curDeckName + u"\" card:" + TemplateNames.clozeTemplateName
            numClozeCards = len(findCards(mw.col, clozeQuery))

            listeningQuery = u"\"deck:" + curDeckName + u"\" card:" + TemplateNames.listeningTemplateName
            numListeningCards = len(findCards(mw.col, listeningQuery))

            if numClozeCards != 0 and numListeningCards != 0:
                curDeck[u"conf"] = pConf
            elif numClozeCards != 0:
                curDeck[u"conf"] = cConf
            elif numListeningCards != 0:
                curDeck[u"conf"] = lConf

            mw.col.decks.save(curDeck)

    @staticmethod
    def getListeningConfigId():
        return JlabOptions._getConfigId(JlabOptions.listeningConfigName)

    @staticmethod
    def getClozeConfigId():
        return JlabOptions._getConfigId(JlabOptions.clozeConfigName)

    @staticmethod
    def getParentConfigId():
        return JlabOptions._getConfigId(JlabOptions.parentConfigName)

    @staticmethod
    def _getConfigId(configName):
        for curItem in mw.col.decks.all_config():
            if curItem[u"name"] == configName:
                return curItem["id"]
        raise ValueError(u"Config not found")

    @staticmethod
    def hasListeningConfig():
        return JlabOptions._hasConfig(JlabOptions.listeningConfigName)

    @staticmethod
    def hasClozeConfig():
        return JlabOptions._hasConfig(JlabOptions.clozeConfigName)

    @staticmethod
    def hasBeginnerParentConfig():
        return JlabOptions._hasConfig(JlabOptions.parentConfigName)

    @staticmethod
    def _hasConfig(configName):
        for curConf in mw.col.decks.all_config():
            if curConf[u"name"] == configName:
                return True
        return False

    listeningConfigName = u"Jlab-Listening"
    clozeConfigName = u"Jlab-Cloze"
    parentConfigName = u"Jlab-Parent" #config name for the parent of the beginner deck

    listeningConfig = {
        u"name": listeningConfigName,
        u"new": {
            u"delays": [5, 20],
            u"ints": [1, 5, 7],  # 7 is not currently used
            u"initialFactor": 2500,
            u"separate": True,
            u"order": 1,
            u"perDay": 15,
            # may not be set on old decks
            u"bury": True,
        },
        u"lapse": {
            u"delays": [10],
            u"mult": 0,
            u"minInt": 1,
            u"leechFails": 99,
            # type 0=suspend, 1=tagonly
            u"leechAction": 1,
        },
        u"rev": {
            u"perDay": 200,
            u"ease4": 1.4,
            u"fuzz": 0.05,
            u"minSpace": 1,  # not currently used
            u"ivlFct": 1,
            u"maxIvl": 36500,
            # may not be set on old decks
            u"bury": True,
        },
        u"maxTaken": 600,
        u"timer": 0,
        u"autoplay": True,
        u"replayq": True,
        u"mod": 0,
        u"usn": 0,
    }

    clozeConfig = {
        u"name": clozeConfigName,
        u"new": {
            u"delays": [5, 20],
            u"ints": [1, 5, 7],  # 7 is not currently used
            u"initialFactor": 2500,
            u"separate": True,
            u"order": 1,
            u"perDay": 15,
            # may not be set on old decks
            u"bury": True,
        },
        u"lapse": {
            u"delays": [10],
            u"mult": 0,
            u"minInt": 1,
            u"leechFails": 99,
            # type 0=suspend, 1=tagonly
            u"leechAction": 1,
        },
        u"rev": {
            u"perDay": 200,
            u"ease4": 1.3,
            u"fuzz": 0.05,
            u"minSpace": 1,  # not currently used
            u"ivlFct": 1,
            u"maxIvl": 36500,
            # may not be set on old decks
            u"bury": True,
        },
        u"maxTaken": 600,
        u"timer": 0,
        u"autoplay": False,
        u"replayq": True,
        u"mod": 0,
        u"usn": 0,
    }

    parentConfig = {
        u"name": clozeConfigName,
        u"new": {
            u"delays": [5, 20],
            u"ints": [1, 5, 7],  # 7 is not currently used
            u"initialFactor": 2500,
            u"separate": True,
            u"order": 1,
            u"perDay": 1000,
            # may not be set on old decks
            u"bury": True,
        },
        u"lapse": {
            u"delays": [10],
            u"mult": 0,
            u"minInt": 1,
            u"leechFails": 99,
            # type 0=suspend, 1=tagonly
            u"leechAction": 1,
        },
        u"rev": {
            u"perDay": 200,
            u"ease4": 1.3,
            u"fuzz": 0.05,
            u"minSpace": 1,  # not currently used
            u"ivlFct": 1,
            u"maxIvl": 36500,
            # may not be set on old decks
            u"bury": True,
        },
        u"maxTaken": 600,
        u"timer": 0,
        u"autoplay": False,
        u"replayq": True,
        u"mod": 0,
        u"usn": 0,
    }

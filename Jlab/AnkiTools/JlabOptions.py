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
            curDeckName = curDeck["name"]

            if curDeckName == _("Default") or curDeckName not in newDeckNameSet:
                continue

            clozeQuery = '"deck:' + curDeckName + '" card:' + TemplateNames.clozeTemplateName
            numClozeCards = len(findCards(mw.col, clozeQuery))

            listeningQuery = '"deck:' + curDeckName + '" card:' + TemplateNames.listeningTemplateName
            numListeningCards = len(findCards(mw.col, listeningQuery))

            if numClozeCards != 0 and numListeningCards != 0:
                curDeck["conf"] = pConf
            elif numClozeCards != 0:
                curDeck["conf"] = cConf
            elif numListeningCards != 0:
                curDeck["conf"] = lConf

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
            if curItem["name"] == configName:
                return curItem["id"]
        raise ValueError("Config not found")

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
            if curConf["name"] == configName:
                return True
        return False

    listeningConfigName = "Jlab-Listening"
    clozeConfigName = "Jlab-Cloze"
    parentConfigName = "Jlab-Parent"  # config name for the parent of the beginner deck

    listeningConfig = {
        "name": listeningConfigName,
        "new": {
            "delays": [5, 20],
            "ints": [1, 5, 7],  # 7 is not currently used
            "initialFactor": 2500,
            "separate": True,
            "order": 1,
            "perDay": 15,
            # may not be set on old decks
            "bury": True,
        },
        "lapse": {
            "delays": [10],
            "mult": 0,
            "minInt": 1,
            "leechFails": 99,
            # type 0=suspend, 1=tagonly
            "leechAction": 1,
        },
        "rev": {
            "perDay": 200,
            "ease4": 1.4,
            "fuzz": 0.05,
            "minSpace": 1,  # not currently used
            "ivlFct": 1,
            "maxIvl": 36500,
            # may not be set on old decks
            "bury": True,
        },
        "maxTaken": 600,
        "timer": 0,
        "autoplay": True,
        "replayq": True,
        "mod": 0,
        "usn": 0,
    }

    clozeConfig = {
        "name": clozeConfigName,
        "new": {
            "delays": [5, 20],
            "ints": [1, 5, 7],  # 7 is not currently used
            "initialFactor": 2500,
            "separate": True,
            "order": 1,
            "perDay": 15,
            # may not be set on old decks
            "bury": True,
        },
        "lapse": {
            "delays": [10],
            "mult": 0,
            "minInt": 1,
            "leechFails": 99,
            # type 0=suspend, 1=tagonly
            "leechAction": 1,
        },
        "rev": {
            "perDay": 200,
            "ease4": 1.3,
            "fuzz": 0.05,
            "minSpace": 1,  # not currently used
            "ivlFct": 1,
            "maxIvl": 36500,
            # may not be set on old decks
            "bury": True,
        },
        "maxTaken": 600,
        "timer": 0,
        "autoplay": False,
        "replayq": True,
        "mod": 0,
        "usn": 0,
    }

    parentConfig = {
        "name": clozeConfigName,
        "new": {
            "delays": [5, 20],
            "ints": [1, 5, 7],  # 7 is not currently used
            "initialFactor": 2500,
            "separate": True,
            "order": 1,
            "perDay": 1000,
            # may not be set on old decks
            "bury": True,
        },
        "lapse": {
            "delays": [10],
            "mult": 0,
            "minInt": 1,
            "leechFails": 99,
            # type 0=suspend, 1=tagonly
            "leechAction": 1,
        },
        "rev": {
            "perDay": 200,
            "ease4": 1.3,
            "fuzz": 0.05,
            "minSpace": 1,  # not currently used
            "ivlFct": 1,
            "maxIvl": 36500,
            # may not be set on old decks
            "bury": True,
        },
        "maxTaken": 600,
        "timer": 0,
        "autoplay": False,
        "replayq": True,
        "mod": 0,
        "usn": 0,
    }

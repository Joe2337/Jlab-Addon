from AnkiTools.JapaneseNoteAccess import *
from aqt.utils import showInfo

class TemplateUpdater:

    # adds furigana to jlab front/back fields (in all templates)
    @staticmethod
    def addFurigana(modelManager):
        for curModel in modelManager.all():
            for curTemplate in curModel["tmpls"]:

                frontConfig = curTemplate["qfmt"]
                for curFieldName in JapaneseNoteAccess.displayFields:
                    frontConfig = frontConfig.replace("{{" + curFieldName + "}}", "{{furigana:" + curFieldName + "}}")
                frontChanged = curTemplate["qfmt"] != frontConfig
                curTemplate["qfmt"] = frontConfig

                backConfig = curTemplate["afmt"]
                for curFieldName in JapaneseNoteAccess.displayFields:
                    backConfig = backConfig.replace("{{" + curFieldName + "}}", "{{furigana:" + curFieldName + "}}")
                backChanged = curTemplate["afmt"] != backConfig
                curTemplate["afmt"] = backConfig

                if not frontChanged and not backChanged:
                    continue

            try:
                modelManager.save(curModel)
            except:
                pass
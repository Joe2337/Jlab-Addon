from AnkiTools.JapaneseNoteAccess import *
from AnkiTools.CardSearch import *
from Core.KanaRoumajiTransliterator import *
from Core.KanaTrainerData import *
from Core.KanjiTrainerData import *
from Core.ReadingAssistanceType import *
from Global.Constants import *
from AnkiTools.TemplateNames import TemplateNames
from aqt import mw
import time

# Important information:
# The templates are stored per note model, i.e. there may be multiple jlab note types and multiple (different!) instances
# of the jlab templates, each with the same name. This is very good for development, as it enables to create different
# jlab cards (with different fields on the cards / different templates), that are all updated by the addon.
# It could, however, also be a source of errors.
class NoteUpdater:
    def __init__(self, settings, kanaTrainerData, kanaRoumajiTransliterator, kanjiTrainerData,
                 kanjiKanaTransliterator, kanjiKanaTransliteratorFull, defensiveKanjiTransliteration, fastCardUpdate):
        self._jlabNoteIds = set()
        self._settings = settings
        self._kanaTrainerData = kanaTrainerData
        self._kanaRoumajiTransliterator = kanaRoumajiTransliterator
        self._kanjiTrainerData = kanjiTrainerData
        self._kanjiKanaTransliterator = kanjiKanaTransliterator
        self._kanjiKanaTransliteratorFull = kanjiKanaTransliteratorFull
        self._defensiveKanjiTranliteration = defensiveKanjiTransliteration
        self._fastCardUpdate = fastCardUpdate
        self._updatingIds = False

    # getting the note ids is a bit slow, therefore they are cached
    def updateJlabNoteIds(self, collection):
        if collection is None:
            raise ValueError("Collection is none")

        listeningCardIds = getListeningCardIds(collection)
        clozeCardIds = getReadingCardIds(collection)

        self._jlabNoteIds = set()
        for cid in listeningCardIds:
            nids = collection.findNotes("cid:" + str(cid))
            if len(nids) != 1:
                raise Exception("Num notes for card != 1")
            self._jlabNoteIds.add(nids[0])
        for cid in clozeCardIds:
            nids = collection.findNotes("cid:" + str(cid))
            if len(nids) != 1:
                raise Exception("Num notes for card != 1")
            self._jlabNoteIds.add(nids[0])

    def updateFieldsOnAllNotes(self, collection):
        if collection is None or collection.decks is None:
            return

        noteIdsForUpdate = set()

        if(self._fastCardUpdate):
            listeningCardInReviewIds = getListeningCardIds(collection, u" -is:new")
            for cid in listeningCardInReviewIds:
                nids = collection.findNotes("cid:" + str(cid))
                if len(nids) != 1:
                    raise Exception("Num notes for card != 1")
                noteIdsForUpdate.add(nids[0])

            # Without the following cards, notes of new listening cards which are immediately suspended are not updated.
            # Consequently, the associated reading cards are not updated.
            listeningCardSuspendedIds = getListeningCardIds(collection, u" is:suspended")
            for cid in listeningCardSuspendedIds:
                nids = collection.findNotes("cid:" + str(cid))
                if len(nids) != 1:
                    raise Exception("Num notes for card != 1")
                noteIdsForUpdate.add(nids[0])

            clozeCardIds = getReadingCardIds(collection, u" -is:new")
            for cid in clozeCardIds:
                nids = collection.findNotes("cid:" + str(cid))
                if len(nids) != 1:
                    raise Exception("Num notes for card != 1")
                noteIdsForUpdate.add(nids[0])

            starterDeckCards = findCards(collection, u"tag:" + TemplateNames.jlabBeginnerTag + u" -card:" + TemplateNames.infoTemplateName)
            for curCard in starterDeckCards:
                noteIdsForUpdate.add(collection.getCard(curCard).nid)
        else:
            self.updateJlabNoteIds(collection)
            noteIdsForUpdate = self._jlabNoteIds # all ids

        numNotes = len(noteIdsForUpdate)

        progress = QProgressDialog(u"Updating cards...", u"Cancel", 0, numNotes, mw)
        progress.setWindowTitle(messageBoxTitle)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()
        QApplication.processEvents() # otherwise the progress bar won't show

        noteCounter = 0

        for noteId in noteIdsForUpdate:
            note = collection.getNote(noteId)

            n = JapaneseNoteAccess(note, collection)
            if not n.isJlabNote():
                raise ValueError("Wrong note type")

            self._updateFields(n, noteCounter)
            noteCounter += 1
            progress.setValue(noteCounter)
            if progress.wasCanceled():
                break

        progress.setValue(numNotes)
        progress.close()

    #Updates only the note that is passed to the function. It is still necessary to iterate over all
    #notes in order to correctly determine the note's position for kana field update (i.e. every nth note in katakana
    #or hiragana)
    def updateFieldsOnSingleNote(self, collection, note):
        noteCounter = 0
        found = False
        for noteId in self._jlabNoteIds:
            if noteId != note.id:
                noteCounter += 1
                continue

            n = JapaneseNoteAccess(note, collection)
            if not n.isJlabNote():
                raise ValueError("Wrong note type")

            self._updateFields(n, noteCounter)
            found = True
            break

        if not found:
            if self._updatingIds == True:
                raise Exception("Note not found")
            else:
                self._updatingIds = True
                self.updateJlabNoteIds(collection)
                self.updateFieldsOnSingleNote(collection, note)
                self._updatingIds = False

    def _getDisplayText(self, hiraganaText, kanjiText, readingAssistanceType, cardCounter):
        if readingAssistanceType == ReadingAssistanceType.none:
            return kanjiText
        elif readingAssistanceType == ReadingAssistanceType.kanjiTrainer:
            furiWithSpace = self._kanjiTrainerData.displayType == KanjiTrainerData.DisplayType.furiganaWithSpace
            furigana, jlab = self._kanjiKanaTransliterator.transliterateSentence(kanjiText, hiraganaText, self._defensiveKanjiTranliteration, furiWithSpace)
            if self._kanjiTrainerData.displayType == KanjiTrainerData.DisplayType.furiganaWithoutSpace or self._kanjiTrainerData.displayType == KanjiTrainerData.DisplayType.furiganaWithSpace:
                return furigana
            elif self._kanjiTrainerData.displayType == KanjiTrainerData.DisplayType.jlab:
                return jlab
            else:
                raise ValueError(u"Not implemented")
        elif readingAssistanceType == ReadingAssistanceType.kanaTrainer:
            kanaType = self._kanaTrainerData.getKanaTypeForDisplay(cardCounter)
            if kanaType == KanaType.katakana:
                hiraganaText = KanaTools.hiraToKata(hiraganaText)
            return self._kanaRoumajiTransliterator.transliterateCard(hiraganaText, u"", False, True)
        elif readingAssistanceType == ReadingAssistanceType.latin:
            return self._kanaRoumajiTransliterator.transliterateCard(hiraganaText, u"", False, False)
        else:
            raise ValueError(u"Not implemented")

    def _getFullFurigana(self, hiraganaText, kanjiText):
        furigana, jlab = self._kanjiKanaTransliteratorFull.transliterateSentence(kanjiText, hiraganaText, self._defensiveKanjiTranliteration, True)
        return furigana

    def _updateFields(self, jlabNoteAccess, cardCounter):
        kanaText = jlabNoteAccess.getHiragana()
        kanaClozeText = jlabNoteAccess.getHiraganaCloze()

        kanjiText = jlabNoteAccess.getSpacedKanji()
        kanjiClozeText = jlabNoteAccess.getKanjiCloze()

        uFrontType = self._settings.listeningFrontReadingAssistance
        uBackType = self._settings.listeningBackReadingAssistance
        cFrontType = self._settings.clozeFrontReadingAssistance
        cBackType = self._settings.clozeBackReadingAssistance

        uFrontText = self._getDisplayText(kanaText, kanjiText, uFrontType, cardCounter)
        uBackText = self._getDisplayText(kanaClozeText, kanjiClozeText, uBackType, cardCounter)
        cFrontText = self._getDisplayText(kanaClozeText, kanjiClozeText, cFrontType, cardCounter)
        cBackText = self._getDisplayText(kanaText, kanjiText, cBackType, cardCounter)

        jlabNoteAccess.setListeningFront(uFrontText)
        jlabNoteAccess.setListeningBack(uBackText)
        jlabNoteAccess.setClozeFront(cFrontText)
        jlabNoteAccess.setClozeBack(cBackText)

        #if len(jlabNoteAccess.getOtherFront()) == 0:
        try:
            jlabNoteAccess.setOtherFront(self._getFullFurigana(kanaText, kanjiText))
        except:
            pass




# Do not remove the unresolved imports, they are found within anki.
from aqt import mw
from aqt.qt import QMessageBox
from AnkiTools.TemplateNames import TemplateNames
from AnkiTools.CardSearch import getListeningCardIds, getReadingCardIds, findCards
from Global.Constants import messageBoxTitle
from AnkiTools.JapaneseNoteAccess import *
from Core.CardEndActionType import CardEndActionType
from Core.Settings import Settings
from aqt.utils import showInfo
from anki.utils import ids2str
from Global.Settings import *

# code for testing, if the suspension intervals make sense. Usage:
# Scheduler.answerCard = wrap(Scheduler.answerCard, checkAfter)
# Reviewer.nextCard = wrap(Reviewer.nextCard, checkBefore)

# cardId = 0
# def checkBefore(self):
#     interval = mw.reviewer.card.ivl
#     repetitions = mw.reviewer.card.reps
#     global cardId
#     cardId = mw.reviewer.card.id
#     if repetitions > 3 and interval >= 9:
#         showInfo(u"Suspend this card: " + str(mw.reviewer.card.ivl) + u" " + str(mw.reviewer.card.reps))
#     else:
#         showInfo(u"cur card: " + str(mw.reviewer.card.ivl) + u" " + str(mw.reviewer.card.reps))
#
# def checkAfter(a, b, c):
#     card = mw.col.getCard(cardId)
#     if card.reps >= 4 and card.ivl > 14:
#         showInfo(u"SUSPENDED: " + str(mw.reviewer.card.ivl) + u" " + str(mw.reviewer.card.reps))

#TODO: explain exactly how and why this works the way it does:
# Which actions are taken? Why are there multiple tags?
class CardManagement:
    gcBaseTag = "jlabgc"
    lcUserTag = gcBaseTag + "::retired-lc"
    clozeUserTag = gcBaseTag + "::retired-cloze"
    lcTouchedTag = gcBaseTag + "::lct"
    clozeTouchedTag = gcBaseTag + "::ct"

    @staticmethod
    def _cardToNoteId(cardIds):
        if mw is None or mw.col is None or mw.col.sched is None:
            return

        result = []
        for cid in cardIds:
            result.append(mw.col.getCard(cid).nid)

        return result

    #from aqt/browser/table/state
    def note_ids_from_card_ids(items):
        return mw.col.db.list(
            f"select distinct nid from cards where id in {ids2str(items)}"
        )


    #test cases
    #for each case, 4 runs gc: gc-no-gc -> same card amount. gc-yes-gc -> nothing remains
    #check in browser if tags are there / not there for beginner!
    #jlab beginner:
    #   suspend 1 lc , do 1 lc beyond ivl -> gc should unsus cloze, nothing else (egal bei welchem setting)
    #       check lc tags
    #   do 1 cloze beyond ivl -> nothing done
    #jlab regular:
    #   suspend 1 lc , do 1 lc beyond ivl -> gc should unsus cloze and tag lc in case of IVL ONLY!
    #       check lc tags: lct 2x, retired-lc 1x
    #   do 1 cloze beyond ivl -> tag/susp/del
    #teppei / delete cloze template
    #   suspend 1 lc , do 1 lc beyond ivl -> gc should delete in case of ivl
    # deactivate, then search for jlabgc
    # activate -> same should happen
    # change settings
    @staticmethod
    def garbageCollectionRegular(settings : Settings):
        if mw is None or mw.col is None or mw.col.sched is None:
            return

        gcProcessedListeningCards, lcWithClozeForEnd, lcWithoutClozeForEnd, clozeCardsForStart, clozeCardsForEnd = CardManagement._getManagedRegularCardAndNoteIds(settings)

        action = settings.endAction

        if settings.endAction not in CardEndActionType.actions:
            raise ValueError("Lifecycle action " + action + " not defined")

        if action != CardEndActionType.delete:
            lcWithClozeForEnd += lcWithoutClozeForEnd #lc without cloze will not be deleted in this case, only tagged / suspended

        if len(lcWithClozeForEnd) == 0 and len(lcWithoutClozeForEnd) == 0 and len(clozeCardsForStart) == 0 and len(clozeCardsForEnd) == 0:
            return

        ret = QMessageBox.StandardButton.Yes
        if settings.promptBeforeCardManagementAction:
            message = u"Card management would:\n\n"
            if len(lcWithClozeForEnd) != 0:
                message += "Tag "
                if action != CardEndActionType.tag:
                    message += "& suspend "
                message += str(len(lcWithClozeForEnd)) + u" listening cards\n"

            if len(clozeCardsForStart) != 0:
                message += u"Unsuspend " + str(len(clozeCardsForStart)) + u" new cloze cards\n"

            if action == CardEndActionType.delete and len(lcWithoutClozeForEnd) != 0:
                message += "Delete " + str(
                    len(lcWithoutClozeForEnd)) + " old listening cards without associated cloze card\n"

            if action == CardEndActionType.delete and len(clozeCardsForEnd) != 0:
                message += "Delete " + str(len(clozeCardsForEnd)) + " old cloze cards (with their listening cards)\n"

            if len(clozeCardsForEnd) != 0 and action != CardEndActionType.delete:
                message += "Tag "
                if action != CardEndActionType.tag:
                    message += "& suspend "
                message += str(len(clozeCardsForEnd)) + u" old cloze cards\n"

            message += "\nProceed?"
            ret = QMessageBox.question(mw, messageBoxTitle, message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if ret == QMessageBox.StandardButton.Yes:
            # Caution: suspending an empty set of card ids causes Anki to reschedule cards that are in the learning
            # queue (i.e. appear red in the deck overview). Their due number is set to the end of the deck.

            mw.col.tags.bulk_add(CardManagement.note_ids_from_card_ids(gcProcessedListeningCards), CardManagement.lcTouchedTag)
            mw.col.tags.bulk_add(CardManagement.note_ids_from_card_ids(clozeCardsForEnd), CardManagement.clozeTouchedTag)

            if len(lcWithClozeForEnd) != 0:
                mw.col.tags.bulk_add(CardManagement.note_ids_from_card_ids(lcWithClozeForEnd), CardManagement.lcUserTag)
                if action != CardEndActionType.tag:
                    mw.col.sched.suspendCards(lcWithClozeForEnd)
            if len(clozeCardsForStart) != 0:
                mw.col.sched.unsuspendCards(clozeCardsForStart)

            if action == CardEndActionType.delete:
                noteIdsForDeletion = CardManagement.note_ids_from_card_ids(lcWithoutClozeForEnd) + CardManagement.note_ids_from_card_ids(clozeCardsForEnd)
                mw.col.remNotes(noteIdsForDeletion)
            else:
                mw.col.tags.bulk_add(CardManagement.note_ids_from_card_ids(clozeCardsForEnd), CardManagement.clozeUserTag)
                if action == CardEndActionType.suspend:
                    mw.col.sched.suspendCards(clozeCardsForEnd)

    @staticmethod
    def _getManagedRegularCardAndNoteIds(settings : Settings):
        listeningCardsBeyond = getListeningCardIds(mw.col, u" -tag:" + CardManagement.lcTouchedTag +
                                                   " prop:ivl>" + str(settings.lcEndInterval))
        listeningCardsUserSuspended = getListeningCardIds(mw.col, u" is:suspended -tag:" + CardManagement.lcTouchedTag)

        gcProcessedListeningCards = set(listeningCardsBeyond).union(set(listeningCardsUserSuspended))

        lcWithClozeForEnd = set()
        lcWithoutClozeForEnd = set()
        clozeCardsForStart = set()
        for cardId in gcProcessedListeningCards:
            curLcCard = mw.col.getCard(cardId)
            isBeginner = curLcCard.note().hasTag(TemplateNames.jlabBeginnerTag)
            clozeCards = getReadingCardIds(mw.col, u" nid:" + str(curLcCard.nid)) #do not add attributes to search here
            if len(clozeCards) == 1:
                curCCard = mw.col.getCard(clozeCards[0])
                if curCCard.type == 0 and curCCard.queue == -1: #card is new and suspended
                    clozeCardsForStart.add(clozeCards[0])
                if not isBeginner and curLcCard.queue != -1: #card is not beginner and not suspended -> do not touch user-suspended cards
                    lcWithClozeForEnd.add(curLcCard.id)
            elif len(clozeCards) == 0 and not isBeginner and curLcCard.queue != -1: #cloze template was deleted or didn't exist (e.g. podcast deck)
                lcWithoutClozeForEnd.add(curLcCard.id)


        clozeCardsForEnd = getReadingCardIds(mw.col, u" -tag:" + CardManagement.clozeTouchedTag +
                                                   " -tag:" + TemplateNames.jlabBeginnerTag +
                                                   " prop:ivl>" + str(settings.clozeEndInterval))

        return list(gcProcessedListeningCards), list(lcWithClozeForEnd), list(lcWithoutClozeForEnd), list(clozeCardsForStart), clozeCardsForEnd

    @staticmethod
    def garbageCollectionBeginner():
        return
        if mw is None or mw.col is None or mw.col.sched is None:
            return

        noteIds = set()

        # listeningCards = getListeningCardIds(mw.col)
        # for cardId in listeningCards:
        #     note = mw.col.getNote(mw.col.getCard(cardId).nid)
        #     if note.hasTag(TemplateNames.jlabBeginnerTag):
        #         noteIds.add(note.id)
        #
        # infoCards = findCards(mw.col, u"card:" + TemplateNames.infoTemplateName)
        # for cardId in infoCards:
        #     note = mw.col.getNote(mw.col.getCard(cardId).nid)
        #     if note.hasTag(TemplateNames.jlabBeginnerTag):
        #         noteIds.add(note.id)
        #showInfo(str(len(listeningCards)) + " " + str(len(infoCards))+ " " + str(len(noteIds)))

        # this code is better, but doesn't work in 2.1.26 (but in 2.1.35). findCards can't find the tagged notes
        allTaggedCards = findCards(mw.col, u"tag:" + TemplateNames.jlabBeginnerTag)
        noteIds = set()
        for curCard in allTaggedCards:
            noteIds.add(mw.col.getCard(curCard).nid)
        # showInfo(str(len(allTaggedCards)) + " " + str(len(noteIds)))

        maxVersion = 0
        for curNoteId in noteIds:
            note = mw.col.getNote(curNoteId)
            n = JapaneseNoteAccess(note, mw.col)
            maxVersion = max(maxVersion, int(n.getFieldContent("Version")))

        oldNoteIds = []
        for curNoteId in noteIds:
            note = mw.col.getNote(curNoteId)
            n = JapaneseNoteAccess(note, mw.col)
            curVersion = int(n.getFieldContent("Version"))
            if curVersion < maxVersion:
                oldNoteIds.append(curNoteId)

        if debugMessages and len(oldNoteIds) != 0:
            showInfo("Will delete " + str(len(oldNoteIds)) + " old beginner deck notes")
        mw.col.remNotes(oldNoteIds)

    @staticmethod
    def activateCardManagement(settings : Settings):
        if mw is None or mw.col is None or mw.col.sched is None:
            return

        clozeCards = getReadingCardIds(mw.col, " is:new")
        mw.col.sched.suspendCards(clozeCards)
        CardManagement.garbageCollectionRegular(settings)


    # revert changes applied by management: unsuspend cards that were suspended, keep user-suspended ones suspended
    # remark: beginner lc cards are never suspended, user suspended cards are suspended and have prop:ivl < addon settings
    @staticmethod
    def deactivateCardManagement():
        if mw is None or mw.col is None or mw.col.sched is None:
            return

        lcCards = getListeningCardIds(mw.col, u" is:suspended -tag:" + TemplateNames.jlabBeginnerTag + " tag:" + CardManagement.lcUserTag)
        mw.col.sched.unsuspendCards(lcCards)

        newClozeCards = getReadingCardIds(mw.col, u" is:suspended is:new")
        mw.col.sched.unsuspendCards(newClozeCards)

        oldClozeCards = getReadingCardIds(mw.col, u" is:suspended -tag:" + TemplateNames.jlabBeginnerTag + " tag:" + CardManagement.clozeUserTag)
        mw.col.sched.unsuspendCards(oldClozeCards)

        mw.col.tags.bulk_remove(mw.col.findNotes("tag:jlabgc"), CardManagement.gcBaseTag)
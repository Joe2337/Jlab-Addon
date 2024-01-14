from Core.KanaTools import *

# Most of the fields used on this note type should be self-explanatory. A few things however are not directly obvious:
# - Why are there two cloze fields (kanji cloze and hiragana cloze)?
#   The same could be asked for JLAB-Hiragana and JLAB-KanjiSpaced. The reason for explicitly storing the kanji and
#   hiragana expression is, that the reading (=hiragana) is determined in a different place by a different application.
#   It would be possible to apply a furigana algorithm of its own here in the plugin for deriving the kanji readings. This
#   however would then compete with the other application.
#
# - What's the purpose of the dictionary lookup field?
#   The field stores expressions/readings that had been looked up and used as cloze. This data is lateron used
#   by the kanji trainer.

class JapaneseNoteAccess:
    _hiraganaFieldName = u"Jlab-Hiragana"
    _hiraganaClozeFieldName = u"Jlab-HiraganaCloze"
    _kanjiClozeFieldName = u"Jlab-KanjiCloze"
    _spacedKanjiFieldName = u"Jlab-KanjiSpaced"
    _listeningFrontFieldName = u"Jlab-ListeningFront"
    _listeningBackFieldName = u"Jlab-ListeningBack"
    _clozeFrontFieldName = u"Jlab-ClozeFront"
    _clozeBackFieldName = u"Jlab-ClozeBack"
    _lemmaFieldName = u"Jlab-Lemma"
    _dictionaryLookupFieldName = u"Jlab-DictionaryLookup"
    _metadataFieldName = u"Jlab-Metadata"
    _otherFrontFieldName = u"Other-Front"

    allFields = { _hiraganaFieldName, _hiraganaClozeFieldName, _kanjiClozeFieldName, _spacedKanjiFieldName,
                 _listeningFrontFieldName, _listeningBackFieldName, _clozeFrontFieldName, _clozeBackFieldName,
                 _lemmaFieldName, _dictionaryLookupFieldName, _metadataFieldName }

    displayFields = { _listeningFrontFieldName, _listeningBackFieldName, _clozeFrontFieldName, _clozeBackFieldName }

    def __init__(self, note, collection):
        self._note = note
        self._collection = collection

    def getFieldIndex(self, fieldName):
        fieldNames = self._collection.models.field_names(self._note.note_type())
        for i, name in enumerate(fieldNames):
            if name == fieldName:
                return i

        raise Exception("Field not found")

    def isJlabNote(self):
        try:
            self.getFieldIndex(JapaneseNoteAccess._hiraganaFieldName)
            self.getFieldIndex(JapaneseNoteAccess._metadataFieldName)
            return True
        except Exception:
            return False

    def getFieldContent(self, fieldName):
        return self._note.fields[self.getFieldIndex(fieldName)]

    def getHiragana(self):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._hiraganaFieldName)
        result = self._note.fields[fieldIndex]
        return result

    def getHiraganaCloze(self):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._hiraganaClozeFieldName)
        result = self._note.fields[fieldIndex]
        return result

    def getKanjiCloze(self):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._kanjiClozeFieldName)
        result = self._note.fields[fieldIndex]
        return result

    def setHiraganaCloze(self, text):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._hiraganaClozeFieldName)
        self._note.fields[fieldIndex] = text
        self._note.flush()

    def setKanjiCloze(self, text):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._kanjiClozeFieldName)
        self._note.fields[fieldIndex] = text
        self._note.flush()

    def setListeningFront(self, text):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._listeningFrontFieldName)
        self._note.fields[fieldIndex] = text
        self._note.flush()

    def setListeningBack(self, text):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._listeningBackFieldName)
        self._note.fields[fieldIndex] = text
        self._note.flush()

    def setClozeFront(self, text):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._clozeFrontFieldName)
        self._note.fields[fieldIndex] = text
        self._note.flush()

    def setClozeBack(self, text):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._clozeBackFieldName)
        self._note.fields[fieldIndex] = text
        self._note.flush()

    def getSpacedKanji(self):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._spacedKanjiFieldName)
        return self._note.fields[fieldIndex]

    def getLemmata(self):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._lemmaFieldName)
        return self._note.fields[fieldIndex]

    def getOtherFront(self):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._otherFrontFieldName)
        return self._note.fields[fieldIndex]

    def setOtherFront(self, text):
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._otherFrontFieldName)
        self._note.fields[fieldIndex] = text
        self._note.flush()

    def appendDictionaryLookup(self, expression, readings):
        entry = expression.strip() + u"~" + readings.strip()
        fieldIndex = self.getFieldIndex(JapaneseNoteAccess._dictionaryLookupFieldName)
        if len(self._note.fields[fieldIndex]) != 0:
            self._note.fields[fieldIndex] += u"|"
        self._note.fields[fieldIndex] += entry
        self._note.flush()

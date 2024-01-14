class TextFormatter:
    _miscMap = {u"archaism": u"arch",
                u"colloquialism": u"coll",
                u"derogatory": u"derog",
                u"manga slang": u"msl",
                u"obsolete term": u"obs",
                u"slang": u"sl",
                u"vulgar expression or word": u"vulg",
                u"familiar language": u"fam",
                u"children's language": u"kid",
                u"female term or language": u"fem",
                u"male term or language": u"male",
                u"rare": u"rare",
                u"honorific or respectful (sonkeigo) language": u"honor",
                u"humble (kenjougo) language": u"humble",
                u"poetical term": u"poet",
                u"word usually written using kana alone": u"kana",
                u"sensitive": u"sens"}

    #Placeholder for clozes for word separation
    clozePlaceholder = u"*"
    clozeStart = u"<font color=\"#00aa00\">("
    clozeStartNoColor = u"<font color="
    clozeEnd = u")</font>"

    @staticmethod
    def formatMisc(miscString):
        token = miscString.split(u",")
        shortened = []
        for t in token:
            try:
                shortened.append(TextFormatter._miscMap[t.strip()])
            except:
                continue

        if len(shortened) == 0:
            return shortened
        else:
            return u"{" + u", ".join(shortened) + u"}"

    @staticmethod
    def wrapTextForCloze(text):
        return TextFormatter.clozeStart + text + TextFormatter.clozeEnd

    @staticmethod
    def formatDictionaryInputForClozeSingleItem(miscGlossTuple, glossLen):
        miscString = miscGlossTuple[0]
        miscString = TextFormatter.formatMisc(miscString)

        glossString = miscGlossTuple[1]
        if len(glossString) > glossLen:
            glossString = glossString[:glossLen]

        if(len(miscString) == 0):
            return glossString
        else:
            return miscString + u" " + glossString

    @staticmethod
    def hasCloze(inputString):
        return inputString.find(TextFormatter.clozeStart) != -1

    @staticmethod
    def extractSingleCloze(inputString):
        startIndex = inputString.find(TextFormatter.clozeStartNoColor)

        if startIndex == -1:
            raise SyntaxError("No cloze found")

        endIndex = inputString.find(TextFormatter.clozeEnd)

        if endIndex == -1:
            raise SyntaxError("No cloze end found")

        cloze = inputString[startIndex:endIndex + len(TextFormatter.clozeEnd)]
        replaced = inputString.replace(cloze, u"*", 1)
        return replaced, cloze

    @staticmethod
    def replaceClozesWithPlaceholder(stringWithClozes):
        allCloses = []
        while TextFormatter.hasCloze(stringWithClozes):
            curCleaned = TextFormatter.extractSingleCloze(stringWithClozes)
            stringWithClozes = curCleaned[0]
            allCloses.append(curCleaned[1])
        return stringWithClozes, allCloses

    @staticmethod
    def replacePlaceholdersWithClozes(stringWithCleanedClozes, allClozes):
        result = stringWithCleanedClozes
        for curClozeHint in allClozes:
            if result.find(TextFormatter.clozePlaceholder) == -1:
                raise SyntaxError(u"Not enough placeholders found")
            result = result.replace(TextFormatter.clozePlaceholder, curClozeHint, 1)
        return result

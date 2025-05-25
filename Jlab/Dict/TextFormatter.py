class TextFormatter:
    _miscMap = {
        "archaism": "arch",
        "colloquialism": "coll",
        "derogatory": "derog",
        "manga slang": "msl",
        "obsolete term": "obs",
        "slang": "sl",
        "vulgar expression or word": "vulg",
        "familiar language": "fam",
        "children's language": "kid",
        "female term or language": "fem",
        "male term or language": "male",
        "rare": "rare",
        "honorific or respectful (sonkeigo) language": "honor",
        "humble (kenjougo) language": "humble",
        "poetical term": "poet",
        "word usually written using kana alone": "kana",
        "sensitive": "sens",
    }

    # Placeholder for clozes for word separation
    clozePlaceholder = "*"
    clozeStart = '<font color="#00aa00">('
    clozeStartNoColor = "<font color="
    clozeEnd = ")</font>"

    @staticmethod
    def formatMisc(miscString):
        token = miscString.split(",")
        shortened = []
        for t in token:
            try:
                shortened.append(TextFormatter._miscMap[t.strip()])
            except:
                continue

        if len(shortened) == 0:
            return shortened
        else:
            return "{" + ", ".join(shortened) + "}"

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

        if len(miscString) == 0:
            return glossString
        else:
            return miscString + " " + glossString

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

        cloze = inputString[startIndex : endIndex + len(TextFormatter.clozeEnd)]
        replaced = inputString.replace(cloze, "*", 1)
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
                raise SyntaxError("Not enough placeholders found")
            result = result.replace(TextFormatter.clozePlaceholder, curClozeHint, 1)
        return result

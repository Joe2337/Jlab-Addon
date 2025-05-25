from AnkiTools.TemplateNames import *


def findCards(collection, query):
    if collection is None:
        return []
    try:
        return collection.find_cards(query)
    except:
        return []


def getListeningCardIds(collection, modifiers=""):
    return findCards(collection, "card:" + TemplateNames.listeningTemplateName + modifiers)


def getReadingCardIds(collection, modifiers=""):
    return findCards(collection, "card:" + TemplateNames.clozeTemplateName + modifiers)

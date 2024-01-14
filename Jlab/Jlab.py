#Hello fellow coder! The source of this addon is particularly nice at some points.
#If you have questions, feel free to reach out to
#joe@japanese-like-a-breeze.com.

from anki.hooks import wrap, addHook
from anki.importing.apkg import *
from anki.importing.apkg import AnkiPackageImporter
from anki import hooks

from aqt import mw
from aqt.qt import *
from aqt.webview import AnkiWebView
from aqt.editor import Editor
from aqt.addons import AddonManager
from aqt.utils import *
from aqt.main import AnkiQt
from aqt.main import AnkiQt
from aqt.utils import showInfo
from aqt.reviewer import Reviewer
from aqt.browser.previewer import Previewer
from aqt.importing import importFile
from aqt import gui_hooks

from AnkiTools.CardManagement import CardManagement
from AnkiTools.JlabOptions import JlabOptions
from AnkiTools.ApkgChecker import ApkgChecker
from AnkiTools.TemplateUpdater import TemplateUpdater
from AnkiTools.TemplateNames import TemplateNames
from Core.CurrentVersion import *
from Core.ClozeEditor import *
from Core.SettingsDialog import *
from Core.KanaTrainer import *
from Core.Settings import *
from Core.SettingsPerApp import *
from Core.KanjiTrainer import *
from Core.KanjiKanaTransliterator import *
from Core.HiddenSettings import *
from Core.WebSearch import WebSearch
from Core.KanjiTrainerData import *
from Core.NoteUpdater import *
from Dict.JapaneseDictionary import *
from Global.Constants import *
from Persistence.FileStorageEngine import *

import io
import webbrowser
import os.path
import subprocess
import aqt
import platform
import base64

#-----------------------------definitions of plugin-relevant variables
fileStorageEngine = FileStorageEngine()

settingsPerApp = SettingsPerApp()

kanaTrainerData = KanaTrainerData()
learnedHiragana = kanaTrainerData.learnedHiragana
learnedKatakana = kanaTrainerData.learnedKatakana
kanaTrainerDataFileName = "KanaTrainerData"

kanjiTrainerData = KanjiTrainerData()
learnedKanji = kanjiTrainerData.learnedKanji
kanjiTrainerDataFileName = "KanjiTrainerData"

settings = Settings()
settingsPerAppFolder = os.path.dirname(os.path.dirname(__file__)) + u"/"
settingsPerAppFileName = u"SettingsPerApp"
settingsFileName = "Settings"

hiddenSettings = HiddenSettings()
hiddenSettingsFileName = "HiddenSettings"

kanaRoumajiTransliterator = KanaRoumajiTransliterator(learnedHiragana, learnedKatakana)

jDictPath = os.path.dirname(__file__) + u"/Data/JDict.sqlite"
jDict = JapaneseDictionary(jDictPath)
kanjiumPath = os.path.dirname(__file__) + u"/Data/kanjidb.sqlite"
kanjium = Kanjium(kanjiumPath)

kanjiKanaTransliterator = KanjiKanaTransliterator(kanjium, learnedKanji)
kanjiKanaTransliteratorFull = KanjiKanaTransliterator(kanjium, LearnedKanji()) #will always create full furigana

apkgConverterExecutable = os.path.dirname(__file__) + u"/Apps/apkgConverter.exe"

noteUpdater = NoteUpdater(settings, kanaTrainerData, kanaRoumajiTransliterator, kanjiTrainerData,
                              kanjiKanaTransliterator, kanjiKanaTransliteratorFull, hiddenSettings.defensiveKanjiReadings,
                              hiddenSettings.fastCardUpdate)

uChecked = False

web = QWebEnginePage()

#-----------------------------definitions of plugin-relevant functions

def getNote():
    if aqt.mw.state == "review":
        return mw.reviewer.card.note()
    else:
        (creator, instance) = aqt.dialogs._dialogs["Browser"]
        if instance is not None and instance._previewer is not None: #in this case, the previewer window is active
            card = instance._previewer.card()
            if card is not None:
                return card.note()
    return None

def getCard():
    if aqt.mw.state == "review":
        return mw.reviewer.card
    else:
        (creator, instance) = aqt.dialogs._dialogs["Browser"]
        if instance is not None and instance._previewer is not None: #in this case, the previewer window is active
            return instance._previewer.card()
    return None

def getSelectedText():
    if aqt.mw.state == "review":
        return mw.web.page().selectedText()
    else:
        (creator, instance) = aqt.dialogs._dialogs["Browser"]
        if instance is not None and instance._previewer is not None: #in this case, the previewer window is active
            return instance._previewer._web.page().selectedText()
    return ""

def unloadDictionaries():
    jDict.close()
    kanjium.close()

def showChangelog():
    content = u""
    with codecs.open(os.path.dirname(__file__) + "/changelog.txt", "r", encoding="utf-8") as file:
        content = file.read()
        content = content.replace("\r\n", "<br>")
        # content = content.replace("<strong>", "<br><br><strong>")
        file.close()

    dialog = QDialog(mw)

    textEdit = QTextEdit(dialog)
    textEdit.setHtml(content)

    dialog.setWindowTitle(messageBoxTitle)
    layout = QVBoxLayout()
    layout.addWidget(textEdit)
    dialog.setLayout(layout)

    dialog.resize(800, 600)
    dialog.exec()
    dialog = None

def linuxMacHint():
    webbrowser.open("https://www.japanese-like-a-breeze.com/linux-mac/")

def showChangelogOnce():
    blockFilePath = mw.addonManager.addonsFolder() + "\\" + str(addonId) + "\\changelogShown.tmp"
    if os.path.exists(blockFilePath):
        return
    showChangelog()
    io.open(blockFilePath, u"wb").close()

def updateDeckBrowser():
    if mw is None or mw.deckBrowser is None:
        return
    try:
        if mw.state == "deckBrowser":
            mw.deckBrowser.refresh()
    except:
        return

def updateReviewer():
    if mw is None or mw.reviewer is None or mw.reviewer.card is None:
        return
    try:
        if mw.col.getCard(mw.reviewer.card.id) is None:
            return
    except:
        return

    mw.reviewer.card.load() #this updates the current card
    mw.moveToState(mw.state) #maybe not necessary, but done in Anki's editor

def updatePreviewer():
    (creator, instance) = aqt.dialogs._dialogs["Browser"]
    if instance is not None and instance._previewer is not None:  # in this case, the previewer window is active
        card = instance._previewer.card()
        if card is None:
            return
        card.load()
        instance._previewer.render_card()

def updateViewers():
    updateReviewer()
    updatePreviewer()

def loadUserData():
    try:
        fileStorageEngine.load(kanaTrainerData, settingsPerApp.getDataFolder(), kanaTrainerDataFileName)
    except IOError:
        pass

    try:
        fileStorageEngine.load(kanjiTrainerData, settingsPerApp.getDataFolder(), kanjiTrainerDataFileName)
    except IOError:
        pass

    try:
        fileStorageEngine.load(settings, settingsPerApp.getDataFolder(), settingsFileName)
    except IOError:
        pass

    try:
        fileStorageEngine.load(hiddenSettings, settingsPerApp.getDataFolder(), hiddenSettingsFileName)
    except IOError:
        fileStorageEngine.save(hiddenSettings, settingsPerApp.getDataFolder(), hiddenSettingsFileName) #write file such that user can set values

    global noteUpdater
    noteUpdater = NoteUpdater(settings, kanaTrainerData, kanaRoumajiTransliterator, kanjiTrainerData,
                              kanjiKanaTransliterator, kanjiKanaTransliteratorFull, hiddenSettings.defensiveKanjiReadings,
                              hiddenSettings.fastCardUpdate)

    if fileStorageEngine.fileOutdated(FileStorageEngine.makePath(settingsPerApp.getDataFolder(), hiddenSettingsFileName), hiddenSettings):
        fileStorageEngine.save(hiddenSettings, settingsPerApp.getDataFolder(), hiddenSettingsFileName) #write file such that user can set new values

def openClozeEditor(selectedText):
    note = getNote()
    if note is None:
        return

    n = JapaneseNoteAccess(note, mw.col)
    japaneseTextAccess = JapaneseTextAccess(n.getHiragana(), n.getSpacedKanji(), n.getHiraganaCloze(),
                                            n.getKanjiCloze(), n.getLemmata(), kanaRoumajiTransliterator,
                                            kanjiKanaTransliterator, kanjium, hiddenSettings.defensiveKanjiReadings)

    clozeEditor = ClozeEditor(japaneseTextAccess, selectedText, learnedHiragana, learnedKatakana, kanaRoumajiTransliterator, jDict, kanjium, settings.clozeEditorReadingAssistance)
    clozeEditor.resize(800, 800)
    if clozeEditor.exec() == QDialog.DialogCode.Rejected:
        clozeEditor = None #not 100% sure, but without setting the qt dialog to none, there might be a memory leak. See https://stackoverflow.com/questions/37918012/pyqt-give-parent-when-creating-a-widget
        return

    n.setHiraganaCloze(clozeEditor.getHiraganaClozeResult())
    n.setKanjiCloze(clozeEditor.getKanjiClozeResult())
    n.appendDictionaryLookup(clozeEditor.getLookedUpExpression(), clozeEditor.getLookedUpReadings())
    noteUpdater.updateFieldsOnSingleNote(mw.col, note)
    clozeEditor = None

    updateViewers()

def onKanaTrainerClicked():
    oldData = copy.deepcopy(kanaTrainerData.toDictionary())
    kanaTrainer = KanaTrainer(kanaTrainerData)
    if kanaTrainer.exec() == 0:
        kanaTrainerData.fromDictionary(oldData)
        kanaTrainer = None
        return

    fileStorageEngine.save(kanaTrainerData, settingsPerApp.getDataFolder(), kanaTrainerDataFileName)
    noteUpdater.updateFieldsOnAllNotes(mw.col)
    kanaTrainer = None

def onKanjiTrainerClicked():
    oldData = copy.deepcopy(kanjiTrainerData.toDictionary())
    kanjiTrainer = KanjiTrainer(kanjiTrainerData)
    if kanjiTrainer.exec() == 0:
        kanjiTrainerData.fromDictionary(oldData)
        kanjiTrainer = None
        return

    fileStorageEngine.save(kanjiTrainerData, settingsPerApp.getDataFolder(), kanjiTrainerDataFileName)
    noteUpdater.updateFieldsOnAllNotes(mw.col)
    kanjiTrainer = None

def runGC():
    if not settings.manageJlabCards:
        return

    try:
        CardManagement.garbageCollectionRegular(settings)
        updateDeckBrowser()
    except Exception as e:
        showInfo("Error: " + str(e))

    LearnedKana._nightMode = mw.pm.night_mode()

def updateAllCards():
    oldVal = noteUpdater._fastCardUpdate
    noteUpdater._fastCardUpdate = False
    noteUpdater.updateFieldsOnAllNotes(mw.col)
    noteUpdater._fastCardUpdate = oldVal

def convertDeck():
    QMessageBox.information(mw, "Information", u"This opens the deck converter, which transforms decks to the jlab format. Please select a deck using \"browse\" in the upper left")
    subprocess.call([apkgConverterExecutable])

def changesClicked():
    WebSearch.openUrl("https://www.japanese-like-a-breeze.com/addon-changes/")

def onSettingsClicked():
    try:
        global settings
        settingsDialog = SettingsDialog(settings)
        settingsDialog.setDataFolder(settingsPerApp.dataFolder)
        if settingsDialog.exec() == 0:
            settingsDialog = None
            return

        #enforce setting of valid data folder
        while(True):
            try:
                settingsPerApp.setDataFolder(settingsDialog.getDataFolder())
                break
            except ValueError:
                QMessageBox.critical(mw, messageBoxTitle, u"Please set a valid data folder")
                settingsDialog.exec()
            except UacError:
                QMessageBox.critical(mw, messageBoxTitle, u"Subfolders in \"Program Files\" or \"Windows\" sometimes cause problems, please choose a different folder.")
                settingsDialog.exec()

        newSettings : Settings = settingsDialog.getSettings()

        if settings.manageJlabCards != newSettings.manageJlabCards:
            if newSettings.manageJlabCards:
                CardManagement.activateCardManagement(newSettings)
            else:
                CardManagement.deactivateCardManagement()
            updateDeckBrowser()

        if settings.clozeEndInterval != newSettings.clozeEndInterval or settings.lcEndInterval != newSettings.lcEndInterval or settings.endAction != newSettings.endAction:
            CardManagement.deactivateCardManagement()
            CardManagement.activateCardManagement(newSettings)
            updateDeckBrowser()

        cardFormatChanged = settings.cardFormatChanged(newSettings)
        settings.fromDictionary(newSettings.toDictionary())
        if cardFormatChanged:
            noteUpdater.updateFieldsOnAllNotes(mw.col)

        fileStorageEngine.save(settings, settingsPerApp.getDataFolder(), u"Settings")
        fileStorageEngine.save(settingsPerApp, settingsPerAppFolder, settingsPerAppFileName)
        settingsDialog = None
    except Exception as e:
        showInfo(str(e))

def mailto():
    ret = QMessageBox.question(mw, messageBoxTitle,
                               "Feel free to send any feedback to:\n" + contactAddress + "\n"
                               "Would you like to send an email now?",
                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if ret == QMessageBox.StandardButton.Yes:
        webbrowser.open('mailto:?to=' + contactAddress, new=1)

def createJapaneseMenu():
    japaneseMenu = mw.menuBar().addMenu(u'&Japanese like a breeze')

    # action = QAction(u"Important changes, please read", mw)
    # action.triggered.connect(changesClicked)
    # japaneseMenu.addAction(action)

    japaneseMenu.addSeparator()

    action = QAction(u"Jlab Settings", mw)
    action.triggered.connect(onSettingsClicked)
    japaneseMenu.addAction(action)

    action = QAction(u"Kana Trainer", mw)
    action.triggered.connect(onKanaTrainerClicked)
    japaneseMenu.addAction(action)

    action = QAction(u"Kanji Trainer", mw)
    action.triggered.connect(onKanjiTrainerClicked)
    japaneseMenu.addAction(action)

    toolsMenu = japaneseMenu.addMenu("Tools")
    action = QAction(u"Run card management", mw)
    action.triggered.connect(runGC)
    toolsMenu.addAction(action)

    action = QAction(u"Update script on all cards", mw)
    action.triggered.connect(updateAllCards)
    toolsMenu.addAction(action)

    action = QAction(u"Convert deck", mw)
    action.triggered.connect(convertDeck)
    toolsMenu.addAction(action)

    japaneseMenu.addSeparator()

    action = QAction(u"Get decks", mw)
    action.triggered.connect(lambda : WebSearch.openUrl("http://japanesedecks.blogspot.com/"))
    japaneseMenu.addAction(action)

    action = QAction(u"User Manual", mw)
    action.triggered.connect(lambda : WebSearch.openUrl("https://ankiweb.net/shared/info/2110939339"))
    japaneseMenu.addAction(action)

    action = QAction(u"Changelog", mw)
    action.triggered.connect(showChangelog)
    japaneseMenu.addAction(action)

    action = QAction(u"Linux and Mac users", mw)
    action.triggered.connect(linuxMacHint)
    japaneseMenu.addAction(action)

    action = QAction("Questions or problems? Contact me!", mw)
    action.triggered.connect(mailto)
    japaneseMenu.addAction(action)

def showJlabTools():
    note = getNote()
    if note is None:
        return

    n = JapaneseNoteAccess(note, mw.col)
    if not n.isJlabNote():
        return

    # TODO: memory management may be crappy here.
    selectedText = getSelectedText()
    #showInfo("A" + str(len(selectedText)))
    if len(selectedText) == 0:
        return

    m = QMenu(mw)

    japaneseTextAccess = JapaneseTextAccess(n.getHiragana(), n.getSpacedKanji(), n.getHiraganaCloze(),
                                            n.getKanjiCloze(), n.getLemmata(), kanaRoumajiTransliterator,
                                            kanjiKanaTransliterator, kanjium, hiddenSettings.defensiveKanjiReadings)

    kanji = japaneseTextAccess.tryMapTo(selectedText, ReadingAssistanceType.none)
    roumaji = japaneseTextAccess.tryMapTo(selectedText, ReadingAssistanceType.latin)

    clozeEditorAction = m.addAction(u"Dictionary / cloze editor")
    clozeEditorAction.triggered.connect(lambda : openClozeEditor(selectedText))

    googleTranslateAction = m.addAction(u"Google translate")
    googleTranslateAction.triggered.connect(lambda : WebSearch.googleTranslate(kanji))

    googleForGrammarAction = m.addAction(u"google for grammar (use kana / kanji)")
    googleForGrammarAction.triggered.connect(lambda : WebSearch.googleForGrammar(selectedText))

    verbixDeinflect = m.addAction(u"Verbix deinflection")
    verbixDeinflect.triggered.connect(lambda : WebSearch.verbixDeinflect(roumaji))

    verbixConjugate = m.addAction(u"Verbix conjugate")
    verbixConjugate.triggered.connect(lambda : WebSearch.verbixConjugate(selectedText))

    m.popup(QCursor.pos())

def updateCurrentNote(self, a, b):
    try:
        note = mw.reviewer.card.note()
        if note is None:
            return

        n = JapaneseNoteAccess(note, mw.col)
        if not n.isJlabNote():
            return

        NoteUpdater.updateFieldsOnSingleNote(mw.col, note)
        updateReviewer()
    except:
        pass

def onLoadedCustomFolderNotExisting():
    QMessageBox.critical(mw, messageBoxTitle, u"The user defined data folder does not exist, please check your settings")
    onSettingsClicked()

def onSettingsPerAppNotFound():
    QMessageBox.information(mw, messageBoxTitle, u"Please specify a folder, where the plugin can store user data.")
    onSettingsClicked()

#this currently is deprecated, as there's no stable import hook.
def changeImportedFile(fileName):
    if fileName[-5:] != ".apkg":
        return fileName, False

    if ApkgChecker.isJlabApkg(fileName):
        return fileName, True

    if "indows" not in platform.system(): #The apkg converter is a windows executable, do not run it on other os
        return fileName, False

    ret = QMessageBox.question(mw, messageBoxTitle,
                               u"Would you like to use this deck with the \"Japanese like a breeze\" addon?",
                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if ret == QMessageBox.StandardButton.Yes:
        base64FileName = str(base64.b64encode(bytes(fileName, 'utf-8')))
        subprocess.call([apkgConverterExecutable, base64FileName])
        convertedFileName = os.path.dirname(fileName) + u"/Converted.apkg"
        if not os.path.isfile(convertedFileName):
            QMessageBox.Critical(mw, messageBoxTitle, u"Could not find converted apkg file (" + convertedFileName + u").")
        return convertedFileName, True
    return fileName, False

deckNames = None
useAddonForNewDeck = False
def beforeImport(mw, file, _old):
    try:
        global deckNames
        deckNames = set(mw.col.decks.allNames())
        JlabOptions.addDefaultConfigurations()
    except:
        pass

    global useAddonForNewDeck
    filename, useAddonForNewDeck = changeImportedFile(file)
    _old(mw, filename)

# allows the importer's background thread to send a message to the ui thread. The note updater's code must be
# executed on the ui thread, because it shows a custom progress bar.
# DEPRECATED, there's currently no stable hook and this keeps breaking...
class ImportThreadConnector(QObject):
    importDone = pyqtSignal()

    def __init__(self):
        super(QObject, self).__init__()
        self.importDone.connect(self.onImportDoneExecOnUiThread)

    def signalImportDone(self):
        self.importDone.emit()

    def onImportDoneExecOnUiThread(self):
        global useAddonForNewDeck
        if not useAddonForNewDeck:
            return

        global deckNames
        if deckNames is not None:
            newDecks = []
            for curDeck in mw.col.decks.allNames():
                if not curDeck in deckNames:
                    newDecks.append(curDeck)
            deckNames = None
            JlabOptions.setOptionsForNewDecks(newDecks)

        TemplateUpdater.addFurigana(mw.col.models)
        if not hiddenSettings.fastCardUpdate:
            noteUpdater.updateFieldsOnAllNotes(mw.col)

importThreadConnector = ImportThreadConnector()

def afterImport(packageImporter):
    importThreadConnector.signalImportDone()

def suspendNewClozeCards(packageImporter):
    if not settings.manageJlabCards:
        return
    try:
        clozeCards = packageImporter.src.findCards(u"card:" + TemplateNames.clozeTemplateName)
        packageImporter.src.sched.suspendCards(clozeCards)
    except:
        return

lastId = 0
def updateCardOnTheFly():
    if not hiddenSettings.fastCardUpdate:
        return

    note = getNote()
    if note is None:
        return

    n = JapaneseNoteAccess(note, mw.col)
    if not n.isJlabNote():
        return

    global lastId
    if lastId == note.id:
        return
    lastId = note.id

    noteUpdater.updateFieldsOnSingleNote(mw.col, note)
    card = getCard()
    if card is not None:
        card.load()

def beforeShowQuestion(reviewer):
    updateCardOnTheFly()

def beforeDeleteAddon(addonManager, dir):
    if dir == str(addonId):
        unloadDictionaries()

timer = QTimer()
timer.timeout.connect(runGC)  # connect it to your update function
timer.setSingleShot(True)
gcExecuted = False
def onDeckBrowserState(self, oldState):
    global gcExecuted
    if not gcExecuted:
        gcExecuted = True
        timer.start(500) #give the main window some time to show

def linkHandlerReviewer(self, url, _old):
    if url == "leftClick":
        showJlabTools()
    else:
        return _old(self, url)

def linkHandlerPreviewer(url):
    if url == "leftClick":
        showJlabTools()
        return

    try:
        (creator, instance) = aqt.dialogs._dialogs["Browser"]
        if instance is None or instance._previewer is None:
            return

        if url == "1":
            instance.set_flag_of_selected_cards(3)
            instance.onNextCard()
            return
        elif url == "2":
            instance.set_flag_of_selected_cards(2)
            instance.onNextCard()
            return
        elif url == "3":
            instance.deleteNotes()
            return
    except:
        return

# test handlers here: https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_document_addeventlistener
def addReviewerHandlers():
    if aqt.mw.state == "review":
        mw.reviewer.web.eval("""document.onclick = () => { pycmd("leftClick"); };""")

#Remark:
# An alternative to global event handlers would be to add a listener. However, this will be done multiple times and is very hard to control:
# instance._previewer._web.eval("""document.addEventListener("click", e => { pycmd("leftClick"); } );""")
# instance._previewer._web.eval("""document.addEventListener("keyup", e => { pycmd(e.key); } );""") # e.code is also available
# Injecting the handlers once also doesn't work, because the web page for display changes frequently, which disables everything again.
def addPreviewerHandlers():
    (creator, instance) = aqt.dialogs._dialogs["Browser"]
    if instance is not None and instance._previewer is not None:  # in this case, the previewer window is active
        instance._previewer._web.set_bridge_command(linkHandlerPreviewer, None)
        instance._previewer._web.eval("""document.onclick = () => { pycmd("leftClick"); };""")
        instance._previewer._web.eval("""document.onkeyup = e => { pycmd(e.key); };""") # e.code is also available

def onCardDidRender(templateRenderOutput, RenderContext):
    addReviewerHandlers()
    addPreviewerHandlers()

#-----------------------------Connect everything to Anki
createJapaneseMenu()

settingsPerApp.folderChanged.connect(loadUserData)
settingsPerApp.loadedCustomFolderNotExisting.connect(onLoadedCustomFolderNotExisting)

# fast card update makes these lines obsolete. Keep them for a while for reference.
#Editor.saveNow = wrap(Editor.saveNow, updateCurrentNote) #TODO: this line works, however, EditCurrent.saveAndClose should be preferred (which doesn't work)
#EditCurrent.saveAndClose = wrap(EditCurrent.saveAndClose, updateCurrentNote)

AnkiQt._deckBrowserState = wrap(AnkiQt._deckBrowserState, onDeckBrowserState)
aqt.importing.importFile = wrap(aqt.importing.importFile, beforeImport, "around")
AnkiPackageImporter.run = wrap(AnkiPackageImporter.run, afterImport) #caution, run is executed on different thread
AnkiPackageImporter._prepareFiles = wrap(AnkiPackageImporter._prepareFiles, suspendNewClozeCards)
Reviewer._showQuestion = wrap(Reviewer._showQuestion, beforeShowQuestion, "before")
Previewer.render_card = wrap(Previewer.render_card, beforeShowQuestion, "before")
AddonManager.deleteAddon = wrap(AddonManager.deleteAddon, beforeDeleteAddon, "before")
Reviewer._linkHandler = wrap(Reviewer._linkHandler, linkHandlerReviewer, 'around') #part of java script bridge

hooks.card_did_render.append(onCardDidRender)

try:
    fileStorageEngine.load(settingsPerApp, settingsPerAppFolder, settingsPerAppFileName) #loading of user data is triggered by a signal in settingsPerApp. It is done, after the user data folder is loaded.
except (IOError, ValueError) as e:
    onSettingsPerAppNotFound()

# in order to check for updates, run aqt.addons.check_and_prompt_for_updates

#-----------------------------Test code, do not delete

def testIt():
    CardManagement.activateCardManagement(settings)
    #showInfo(platform.system())
    #JlabOptions.addDefaultConfigurations()
    #TemplateUpdater.addFurigana(mw.col.models)

def testIt2():
    try:
        CardManagement.deactivateCardManagement()
    except Exception as e:
        showInfo(str(e))
    #showInfo(platform.system())
    #JlabOptions.addDefaultConfigurations()
    #TemplateUpdater.addFurigana(mw.col.models)

#from AnkiTools.CardManagement2 import CardManagement2
# def testIt3():
#     try:
#         CardManagement2.garbageCollectionRegular()
#     except Exception as e:
#         showInfo(str(e))
#
# action = QAction(u"act", mw)
# action.triggered.connect(testIt)
# mw.form.menuTools.addAction(action)
#
# action2= QAction(u"deact", mw)
# action2.triggered.connect(testIt2)
# mw.form.menuTools.addAction(action2)
#
# action3= QAction(u"oldgc", mw)
# action3.triggered.connect(testIt3)
# mw.form.menuTools.addAction(action3)

# def testCardManagementBasics():
#     #mw.col.sched.unsuspendCards(mw.col.findCards(u"card:" + TemplateNames.listeningTemplateName))
#     #mw.col.sched.suspendCards(mw.col.findCards(u"card:" + TemplateNames.listeningTemplateName))
#     #mw.col.remCards(mw.col.findCards(u"card:" + TemplateNames.listeningTemplateName))
#     #mw.reset()
#     return
# action = QAction(u"test card management basics", mw)
# action.triggered.connect(testCardManagementBasics)
# mw.form.menuTools.addAction(action)


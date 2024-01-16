

# Readme
This repository contains the main code and data for the Jlab Anki addon. 

Core components of the plugin are developed in the package Jlab. The file Jlab/Jlab.py is the main entry point.

The deck converter used by the addon is not part of this repository. It was written in c++ for historical reasons and is shipped as separate app. 

The project does not build Anki. This means that it is not possible to test/debug the addon within Anki from the IDE. Instead, I directly test everything in Anki. There's a deploy script available that copies everything to Anki's plugin folder.

## Build and run
- Install visual studio code and anaconda
- Open an anaconda prompt
- Create a virtual environment in the anaconda prompt: conda create -n jlabdev python=3.9
- Activate this venv from the anaconda prompt: conda activate jlabdev
- Start vs code from this window with the activated venv
- pip install PyQt6
- pip install pyqt6-tools
- Install python plugin for vs code
- Before running the plugin, you need to build the ui. This done by running /Jlab/Core/buildUi.py
- Running manual tests: main.py
- Running automatic tests: automaticTests.py
- Reploying everything to Anki: deployment.py. Use the following launch config in vs code (adapt your paths):
```json
{
   "version":"0.2.0",
   "configurations":[
      {
         "name":"Deploy to Anki",
         "type":"python",
         "request":"launch",
         "program":"enter your path to deployment.py",
         "console":"integratedTerminal",
         "env":{
            "PYTHONPATH":"enter your path to repository/jlab"
         },
         "args":[
            "C:\\Users\\Joe\\AppData\\Roaming\\Anki2\\addons21\\2110939339\\"
         ]
      }
   ]
}
```
## Automatic testing
The project has several tests in the autotest subfolder. Most important are those for the script conversion, where errors are easily introduced and are hard to tackle. Improvements quickly introduce new errors somewhere else. See automaticTests.py.

## Manual testing
- To check problems with globally installed libraries / other operating systems: Move everything to a virtual test system (system without any libs, runtimes, etc installed - usually not necessary)
- Install latest anki
- Set Global.Settings.debugMessages = true
- Rename the old settingsperapp.json
- Delete user profile to have fully empty folder
- Start Anki, install addon, then restart Anki
- Set data folder in "program files" -> should not work
- Import non-jlab deck (see misc folder) with yes and no, no first (caused a bug with the collection before). Are non-jlab-cards working?
- Import beginner's course
- Test the jlab decks with fast card update: Check, if new cards are updated on the fly. They do not have any text text on the front field, but are updated right before the reviewer shows them.
- Test the jlab decks with fast card update: Is the card content correct?
	- After changes in SettingsDialog
	- After changes in KanaTrainer
	- After changes in KanjiTrainer -> make sure to check furigana
	- After import
- Test the kanji trainer: Apply to all cards
- Test fast card update for non-new cards: Fast card update must update all of them. This must be checked in the card browser after settings where changed. Create non-new cards by reviewing some new ones
- Change options of first jlab deck, then import a new deck (while anki is already running to make sure cached data in NoteUpdater is correctly updated):
	- New cloze cards must be suspended
	- Deck must have jlab default options
	- Furigana must work
	- New card content must be updated in reviewer according to reading assistance (if this doesn't work, cached data in NoteUpdater is outdated)
	- Options of first deck must not be changed 
- Card management:
	- Activate in settings and change the intervals to 3 days (reading cards should be active, cloze cards suspended)
	- Do a reading card beyond 3 days, then run card management (1 cloze card should be unsuspended)
	- Do the cloze card beyond 3 days, then run card management (cloze card should be suspended again)
	- Deactivate / activate again and see if cards are suspended / unsuspended
	- Beginner's course cards do not have an end action
- Check, if addon works on previewer (secret feature ;))
- Perform update (by modifying mod number in meta.json -> backup local addon before)
- Update different addon (1873344186), jlab must work afterwards (dictionary!)
- Delete different addon, jlab must work afterwards
- Uninstall addon

- Set Global.Settings.debugMessages = False
	
## Release
- Update changelog.txt
- Build the python ui
- Python tests:
	- Make sure no auto test is commented out and run them
	- Set Global.Settings.debugMessages = false
	- Make sure all debug code is commented out, in particular the Jlab.testIt()
- Increment version number in the source code
- Deploy the python code
- Compile and deploy c++ apps
- Test everything -> see "testing"
- Remove meta.json, if updating from anki
- Zip everything
- Put update to on ankiweb

import codecs
import os.path
import json

from Persistence.IStorageEngine import *

from Persistence.IStorable import *


class FileStorageEngine(IStorageEngine):

    @staticmethod
    def makePath(folder, filename):
        return folder + u"/" + filename + u".json"

    def save(self, iStorable, folder, filename):
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.saveToFile(FileStorageEngine.makePath(folder, filename), iStorable)

    def load(self, iStorable, folder, filename):
        self.loadFromFile(FileStorageEngine.makePath(folder, filename), iStorable)

    def saveToFile(self, path, iStorable):
        with codecs.open(path, "w", encoding="utf-8") as file:
            file.write(json.dumps(iStorable.toDictionary(), indent=4))
            file.close()

    def loadFromFile(self, path, iStorable):
        content = u""
        with codecs.open(path, "r", encoding="utf-8") as file:
            content = file.read()
            file.close()
        dictionary = json.loads(content)
        iStorable.fromDictionary(dictionary)

    def _dict0Outdated(self, dict0, dict1):
        v0 = dict0["version"]
        v1 = dict1["version"]

        if v0 > v1:
            raise ValueError("dict 0 is newer than dict 1") # this means that a saved istorable is newer than the instantiated istorable, which must never happen

        if v0 < v1:
            return True

        for key, value in dict1.items():
            if isinstance(value, dict):
                return self._dict0Outdated(dict0[key], value)

        return False

    def fileOutdated(self, path, iStorable):
        content = u""
        with codecs.open(path, "r", encoding="utf-8") as file:
            content = file.read()
            file.close()
        dictionaryFile = json.loads(content)
        dictionaryMem = iStorable.toDictionary()

        return self._dict0Outdated(dictionaryFile, dictionaryMem)





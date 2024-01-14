import zipfile
import io
import tempfile
import os
import sqlite3
from AnkiTools.JapaneseNoteAccess import JapaneseNoteAccess

class ApkgChecker:
    @staticmethod
    def isJlabApkg(path):
        z = zipfile.ZipFile(path)
        col = z.read("collection.anki2")

        (fd, name) = tempfile.mkstemp()
        os.close(fd)
        with open(name, 'wb') as f:
            f.write(col)

        db = sqlite3.connect(name)
        cursor = db.cursor()
        cursor.execute('select models from col')
        #cursor.execute('SELECT name from sqlite_master where type= "table"')

        queryResult = cursor.fetchall()
        if len(queryResult) != 1:
            raise ValueError(u"Model search result length != 1")
        modelString = queryResult[0][0]

        db.close()
        os.remove(name)

        result = True
        for curFieldName in JapaneseNoteAccess.allFields:
            result = result and modelString.find(curFieldName) != -1
        return result

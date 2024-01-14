import sqlite3
import os.path

class JapaneseDictionary:
    def __init__(self, path = u""):
        if len(path) == 0:
            path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) +u"/Data/JDict.sqlite"
        if not os.path.isfile(path):
            raise Exception(u"Invalid path: " + path)
        self._db = sqlite3.connect(path, check_same_thread=False)

    def close(self):
        self._db.close()

    def lookup(self, query):
        cursor = self._db.cursor()
        cursor.execute('select JGroup.Expressions, JGroup.Readings, JGroup.Misc, JGroup.XRef, Sense.Gloss '
                       'from JExpressions '
                       'inner join JLookup on JLookup.JExpressionId = JExpressions.Id '
                       'inner join JDict on JLookup.JDictId = JDict.Id '
                       'inner join JGroup on JDict.JGroupId = JGroup.Id '
                       'inner join Sense on JDict.SenseId = Sense.Id '
                       'where Expression = ?', [query])

        return cursor.fetchall()
        rows = cursor.fetchall()
        for row in rows:
            print(row[4])

    def getAllReadings(self):
        cursor = self._db.cursor()
        cursor.execute('select JGroup.Readings, JGroup.Id '
                       'from JExpressions '
                       'inner join JLookup on JLookup.JExpressionId = JExpressions.Id '
                       'inner join JDict on JLookup.JDictId = JDict.Id '
                       'inner join JGroup on JDict.JGroupId = JGroup.Id '
                       'inner join Sense on JDict.SenseId = Sense.Id ')

        result = set()
        for x in cursor.fetchall():
            result.add(x)
        return result

    def getExpressionAndReadingOfAllEntries(self):
        cursor = self._db.cursor()
        cursor.execute('select JGroup.Expressions, JGroup.Readings, JGroup.Misc '
                       'from JGroup ')

        return cursor.fetchall()

#TODO: When upgrading to anki 2.1, this can be replaced with newer versions, see:
#https://stackoverflow.com/questions/13646245/is-it-possible-to-make-abstract-classes-in-python

from abc import ABCMeta, abstractmethod

#Splitting into IStorable and IStorageEngine allows to serialize only selected class members.
class IStorageEngine:
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, iStorable, filename):
        pass

    @abstractmethod
    def load(self, iStorable, filename):
        pass

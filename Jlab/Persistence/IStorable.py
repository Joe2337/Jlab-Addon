#TODO: When upgrading to anki 2.1, this can be replaced with newer versions, see:
#https://stackoverflow.com/questions/13646245/is-it-possible-to-make-abstract-classes-in-python

from abc import ABCMeta, abstractmethod
import collections #todo: remove

class IStorable:

    # self.version must be set by subclasses and stores the currenly serialized class version.
    # It must be saved to the dictionary returned by IStorable.toDictionary and loaded / handled by
    # IStorable.toDictionary. Note, that IStorable.toDictionary must not deserialize version
    # to self.version, but a local member.
    # A better storage interface would handle versioning automatically,
    # similar to the c++ boost / cereal libraries (i.e. without the need for explicitly loading the version in each
    # subclass). But for the sake of simplicity, this should do the job, too.
    def getVersion(self):
        return self.version

    # identifier that should serve as "what's this" in the stored file.
    def getIdentifier(self):
        try:
            return self._identifier
        except AttributeError:
            return self.__class__.__name__

    @abstractmethod
    def toDictionary(self):
        pass

    @abstractmethod
    def fromDictionary(self, dictionary):
        pass
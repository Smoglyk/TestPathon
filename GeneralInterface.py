from abc import ABC, abstractmethod

class AbstractFormat(ABC):

    @abstractmethod
    def dump(self, obj, fp):
        pass
    @abstractmethod
    def dumps(self, obj)->str:
        pass
    @abstractmethod
    def load(self, fp):
        pass
    @abstractmethod
    def loads(self,str_json):
        pass
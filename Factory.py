from abc import ABC, abstractmethod
from GeneralInterface import AbstractFormat
from Myjson import JsonFormat

class Factory(ABC):

    @abstractmethod
    def create_serializer(self)->AbstractFormat:
        pass

    def SomeOperation(self):
        serializer = self.create_serializer()


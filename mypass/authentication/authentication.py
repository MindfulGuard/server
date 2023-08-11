from abc import ABCMeta, abstractmethod

class Authentication(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):pass
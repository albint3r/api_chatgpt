from abc import ABC, abstractmethod

from config import APIConfiguration


class ICompletionFacade(ABC):

    @abstractmethod
    def create(self, *, prompt: str):
        NotImplementedError()

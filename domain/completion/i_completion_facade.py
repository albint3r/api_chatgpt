from abc import ABC, abstractmethod


class ICompletionFacade(ABC):

    @abstractmethod
    def create(self, *, prompt: str):
        NotImplementedError()

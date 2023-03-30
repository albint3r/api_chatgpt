from abc import ABC, abstractmethod


class IDalleImgFacade(ABC):

    @abstractmethod
    def create(self, *, prompt: str):
        NotImplementedError()

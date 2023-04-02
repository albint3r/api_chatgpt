from abc import ABC, abstractmethod


class IChatBotFacade(ABC):

    @abstractmethod
    def run(self):
        NotImplementedError()

from abc import ABC, abstractmethod


class IDalleImgFacade(ABC):

    @abstractmethod
    def run(self):
        NotImplementedError()

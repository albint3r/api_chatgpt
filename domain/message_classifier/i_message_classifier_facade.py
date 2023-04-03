from abc import ABC, abstractmethod

from config import APIConfiguration
from domain.chat_bot.message import Message


class IMessageClassifierFacade(ABC):

    @abstractmethod
    def predict(self, msg: Message):
        NotImplementedError()

    @abstractmethod
    def initialize(self, config: APIConfiguration):
        NotImplementedError()

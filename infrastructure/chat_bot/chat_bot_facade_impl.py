import openai
from injector import inject

from config import APIConfiguration
from domain.chat_bot.chat import Chat
from domain.chat_bot.prediction import Prediction
from domain.chat_bot.i_chat_bot_facade import IChatBotFacade
from domain.chat_bot.message import Message


class ChatBotFacade(IChatBotFacade):
    """
    A class representing the ChatBotFacade, which is responsible for managing the chatbot interaction.

    Attributes:
    ----------
    config : APIConfiguration
        The API configuration object containing the necessary API key.
    """
    @inject
    def __init__(self, config: APIConfiguration):
        """
        Initialize the ChatBotFacade with the provided API configuration.

        Parameters:
        ----------
        config : APIConfiguration
            The API configuration object containing the necessary API key.
        """
        self.config: APIConfiguration = config

    def run(self) -> None:
        """
        Start and run the chatbot conversation until it is finished.
        """
        openai.api_key = self.config.api_key
        chat = Chat()
        while not chat.is_finished:
            user_msg = Message.from_user(prompt=chat.input_user())
            chat.add(user_msg)
            prediction_response = openai.ChatCompletion.create(
                model=chat.model,
                messages=chat.messages
            )
            prediction = Prediction.from_json(prediction_response)
            assistant_msg = Message.from_assistant(prediction.message)
            chat.add(assistant_msg)
            chat.show()

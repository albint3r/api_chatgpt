import openai
from injector import inject

from config import APIConfiguration
from domain.chat_bot.chat import Chat
from domain.chat_bot.prediction import Prediction
from domain.chat_bot.i_chat_bot_facade import IChatBotFacade
from domain.chat_bot.message import Message
from infrastructure.message_classifier.message_classifier_facade_impl import MessageClassifierFacadeImpl


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
        # Create New Chat
        chat = Chat(config=self.config, verbose=False)
        while not chat.is_finished:
            user_msg = Message.from_user(prompt=chat.prompt_user())
            chat.add(user_msg)
            assistant_msg = chat.process_message_response()
            chat.add(assistant_msg)
            chat.show()
            # If the Chat is above 1k tokens it will be resumed to maintain the conversation context
            chat.update_resume_chat(call_back=openai.Completion.create)

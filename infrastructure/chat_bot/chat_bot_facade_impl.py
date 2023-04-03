import openai
from injector import inject

from config import APIConfiguration
from domain.chat_bot.chat import Chat
from domain.chat_bot.prediction import Prediction
from domain.chat_bot.i_chat_bot_facade import IChatBotFacade
from domain.chat_bot.message import Message
from infrastructure.message_classifier.topic_predictor_facade_impl import MessageClassifierFacade


class ChatBotFacade(IChatBotFacade):
    """
    A class representing the ChatBotFacade, which is responsible for managing the chatbot interaction.

    Attributes:
    ----------
    config : APIConfiguration
        The API configuration object containing the necessary API key.
    """

    @inject
    def __init__(self, config: APIConfiguration, msg_classifier: MessageClassifierFacade):
        """
        Initialize the ChatBotFacade with the provided API configuration.

        Parameters:
        ----------
        config : APIConfiguration
            The API configuration object containing the necessary API key.
        """
        self.config: APIConfiguration = config
        self.msg_classifier: MessageClassifierFacade = msg_classifier

    def run(self) -> None:
        """
        Start and run the chatbot conversation until it is finished.
        """
        openai.api_key = self.config.api_key
        # Initialize Topic Predictor
        self.msg_classifier.initialize(self.config)
        # Create New Chat
        chat = Chat(verbose=False)
        while not chat.is_finished:
            user_msg = Message.from_user(prompt=chat.input_user())
            chat.add(user_msg)
            topic_prediction = self.msg_classifier.predict(user_msg)
            print(topic_prediction)
            prediction_response = openai.ChatCompletion.create(
                model=chat.model,
                messages=chat.messages
            )
            prediction = Prediction.from_json(prediction_response)
            chat.update_used_tokens(prediction.total_tokens)
            assistant_msg = Message.from_assistant(prediction.message)
            chat.add(assistant_msg)
            chat.show()
            # If the Chat is above 1k tokens it will be resumed to maintain the conversation context
            chat.update_resume_chat(call_back=openai.Completion.create)

import os
from dataclasses import dataclass, field
from typing import Callable

import openai

from config import APIConfiguration
from domain._json_serialize import JsonSerialize
from domain.chat_bot.message import Message
from domain.chat_bot.prediction import Prediction
from domain.completion.completion_response import CompletionResponse
from infrastructure.message_classifier.message_classifier_facade_impl import MessageClassifierFacadeImpl


@dataclass
class Chat(JsonSerialize):
    """
    A class representing a Chat object, which stores a conversation between a user and an AI assistant.

    Attributes:
    ----------
    _current_chat : list[Message] | None
        A list of Message objects representing the conversation, or None if the chat has not started.
    _history_chat : list[Message]
        A list of Message objects representing the entire conversation history.
    _model : str
        The AI model used for the conversation, default is "gpt-3.5-turbo".
    _prefix : str
        The prefix used to indicate user input, default is ">:"
    _is_finished : bool
        Indicates if the chat has ended, default is False.
    _used_tokens : int
        The number of tokens used in the chat, default is 0.
    _max_tokens : int
        The maximum number of tokens allowed in the chat, default is 400.
    """

    config: APIConfiguration
    verbose: bool = field(kw_only=True, default=False)
    _current_chat: list[Message] | None = field(init=False)
    _history_chat: list[Message] | None = field(init=False, default_factory=list)
    _model: str = field(default="gpt-3.5-turbo")
    _prefix: str = field(default=">:")
    _is_finished: bool = False
    _used_tokens: int = 0
    _max_tokens: int = 1000

    def __post_init__(self):
        """Initialize the starting messages in the chat."""
        self._init_current_chat()

    @property
    def model(self) -> str:
        """Get the AI model used in the chat."""
        return self._model

    @property
    def history(self) -> list[Message]:
        return self._history_chat

    @property
    def last_message(self) -> Message:
        return self._history_chat[-1]

    @property
    def used_tokens(self) -> int:
        """Get the AI model used in the chat."""
        return self._used_tokens

    @used_tokens.setter
    def used_tokens(self, value: int) -> None:
        """Set the number of used tokens in the chat.

        Parameters:
        ----------
        value : int
            The number of tokens used in the chat.

        Raises:
        ------
        ValueError
            If the provided value is negative.

        Returns:
        -------
        None
        """
        if value < 0:
            raise ValueError("Used tokens must be a non-negative integer.")
        self._used_tokens += value

    @property
    def is_finished(self) -> bool:
        """Get the chat's finished status."""
        return self._is_finished

    @property
    def messages(self) -> list[dict[str, str]]:
        """Get the chat messages as a list of JSON-formatted dictionaries."""

        return [msg.to_json() for msg in self._current_chat]

    def _init_current_chat(self) -> None:
        """Initialize the starting messages in the chat as Message objects."""
        STARTING_MSG = [
            {"role": "system", "content": "Pretend you are a expert on Real estates in Mexico, marketing and sales. Be "
                                          "an expert in the INEGI Mexico Data, also"
                                          "Playfully and formal and allways answer in spanish:"},
            {"role": "assistant", "content": "OK"},
        ]
        self._current_chat = [Message.from_json(json) for json in STARTING_MSG]

    def _get_message_classification(self, message: Message):
        msg_classifier = MessageClassifierFacadeImpl()
        msg_classifier.initialize(self.config)
        return msg_classifier.predict(message)

    def _chat_completion_create(self) -> Prediction:
        openai.api_key = self.config.api_key
        prediction_response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        return Prediction.from_json(prediction_response)

    def process_message_response(self) -> Message:
        # TODO DO IT SOMETHING WITH THE MESSAGE -> message
        # TODO DO IT SOMETHING WITH THE MESSAGE -> _get_message_classification
        prediction = self._chat_completion_create()
        self.update_used_tokens(prediction.total_tokens)
        return Message.from_assistant(prediction.message)

    def update_used_tokens(self, current_used_tokens: int) -> None:
        """Update the number of used tokens in the chat.

        Parameters:
        ----------
        current_used_tokens : int
            The number of tokens used in the chat.

        Raises:
        ------
        ValueError
            If the provided value is negative.

        Returns:
        -------
        None
        """
        self.used_tokens = current_used_tokens

    def prompt_user(self) -> str:
        """Prompt the user for input and return the entered text."""
        return input(self._prefix)

    def resume_current_chat(self, *, call_back: Callable, temperature: float) -> CompletionResponse:
        corpus: str = f'Genera un Resumen de los puntos mas importantes de {round(self._max_tokens / 3)} tokens del ' \
                      f'chat entre el usuario y el asistente '
        if self.used_tokens >= self._max_tokens:
            for msg in self.history:
                corpus += msg.content + ' '
            # Resumes corpus
            response = call_back(model="text-davinci-003",
                                 prompt=corpus,
                                 temperature=temperature,
                                 max_tokens=self._max_tokens)

            return CompletionResponse.from_json(response)

    def add_resume_to_chat(self, completion: CompletionResponse) -> None:
        # Convert Completion to Msg
        if self.used_tokens >= self._max_tokens:
            assistant_msg = Message.from_assistant(completion.message)
            # Reset the Current Chat
            self._init_current_chat()
            # Select the last two conversations
            last_two_msg = self._history_chat[2:]
            # Add the resume to the Reset current Chat
            self._current_chat.append(assistant_msg)
            # Add the Last two chats.
            self._current_chat.extend(last_two_msg)
            if self.verbose:
                print(f'TOKENS AREA ABOVE THE MAX LIMIT: {self.used_tokens}')
                print(self._current_chat)

    def update_resume_chat(self, *, call_back: Callable, temperature: float = .2) -> None:
        """Update the chat with a summary of the most important points of the conversation.

        Parameters:
        ----------
        call_back : Callable
            The callback function to resume the chat.
        temperature : float, optional
            The temperature to use in the completion, by default 0.2.

        Returns:
        -------
        None
        """
        completion = self.resume_current_chat(call_back=call_back, temperature=temperature)
        self.add_resume_to_chat(completion)

    def add(self, msg: Message) -> None:
        """ Add a message to the current chat and history chat.

        Parameters:
        ----------
        msg : Message
            The message object to be added to the chat.
        """
        self._current_chat.append(msg)
        self._history_chat.append(msg)

    def show(self) -> None:
        """ Display the chat messages, excluding the first two system messages. """

        if not self.verbose:
            os.system('clear')
        print('Tobe ChatBot')
        print(f'Used Tokens: {self.used_tokens}')
        print('*' * 100)
        for msg in self.history:
            msg.show()
        print('*' * 100)

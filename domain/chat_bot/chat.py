from dataclasses import dataclass, field

from domain._json_serialize import JsonSerialize
from domain.chat_bot.message import Message


@dataclass
class Chat(JsonSerialize):
    """
    A class representing a Chat object, which stores a conversation between a user and an AI assistant.

    Attributes:
    ----------
    _current_chat : list[Message] | None
        A list of Message objects representing the conversation, or None if the chat has not started.
    _model : str
        The AI model used for the conversation, default is "gpt-3.5-turbo".
    _prefix : str
        The prefix used to indicate user input, default is ">:"
    _is_finished : bool
        Indicates if the chat has ended, default is False.
    """
    _current_chat: list[Message] | None = field(init=False)
    _model: str = field(default="gpt-3.5-turbo")
    _prefix: str = field(default=">:")
    _is_finished: bool = False

    def __post_init__(self):
        """Initialize the starting messages in the chat."""
        self._init_starting_msg()

    @property
    def model(self) -> str:
        """Get the AI model used in the chat."""
        return self._model

    @property
    def is_finished(self) -> bool:
        """Get the chat's finished status."""
        return self._is_finished

    @property
    def messages(self) -> list[dict[str, str]]:
        """Get the chat messages as a list of JSON-formatted dictionaries."""

        return [msg.to_json() for msg in self._current_chat]

    def _init_starting_msg(self) -> None:
        """Initialize the starting messages in the chat as Message objects."""
        STARTING_MSG = [
            {"role": "system", "content": "Pretend you are a expert on Real estates, marketing and sales. Be "
                                          "Playfully and formal and allways answer in spanish:"},
            {"role": "assistant", "content": "OK"},
        ]
        self._current_chat = [Message.from_json(json) for json in STARTING_MSG]

    def input_user(self) -> str:
        """Prompt the user for input and return the entered text."""
        return input(self._prefix)

    def add(self, msg: Message) -> None:
        """ Add a message to the current chat.

        Parameters:
        ----------
        msg : Message
            The message object to be added to the chat.
        """
        self._current_chat.append(msg)

    def show(self) -> None:
        """ Display the chat messages, excluding the first two system messages. """
        print('Tobe ChatBot')
        print('*' * 100)
        for msg in self._current_chat[2:]:
            msg.show()
        print('*' * 100)

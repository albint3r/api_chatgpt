from dataclasses import dataclass

from domain._json_serialize import JsonSerialize


@dataclass
class Message(JsonSerialize):
    """
    A class representing a Message object in a Chat conversation.

    Attributes:
    ----------
    role : str
        The role of the message sender, either "user" or "assistant".
    content : str
        The content of the message.
    """
    role: str
    content: str

    @classmethod
    def from_user(cls, prompt: str):
        """ Create a Message object with the "user" role.

        Parameters:
        ----------
        prompt : str
            The content of the user's message.

        Returns:
        -------
        Message
            A Message object with the role set to "user" and the provided content.
        """
        return cls('user', prompt)

    @classmethod
    def from_assistant(cls, prompt: str):
        """ Create a Message object with the "assistant" role.

        Parameters:
        ----------
        prompt : str
            The content of the assistant's message.

        Returns:
        -------
        Message
            A Message object with the role set to "assistant" and the provided content.
        """
        return cls('assistant', prompt)

    def show(self) -> None:
        """ Display the message in the format "Role: Content" followed by a separator line."""
        print(f'{self.role.title()}: {self.content}')
        print('-'*100)

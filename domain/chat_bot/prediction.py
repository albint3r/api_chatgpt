from dataclasses import dataclass

from domain._json_serialize import JsonSerialize


@dataclass
class Prediction(JsonSerialize):
    """
    A class representing a Prediction object from an AI model.

    Attributes:
    ----------
    id : str
        The unique identifier for the prediction.
    object : str
        The type of object, in this case, "prediction".
    created : int
        The Unix timestamp for when the prediction was created.
    model : str
        The AI model used for generating the prediction.
    usage : dict[str, int]
        A dictionary containing information about usage, including "prompt_tokens", "completion_tokens", and "total_tokens".
    choices : list[dict[str, any]]
        A list of dictionaries containing information about the generated choices.
    """
    id: str
    object: str
    created: int
    model: str
    usage: dict[str, int]
    choices: list[dict[str, any]]

    @property
    def message(self):
        """
        Get the content of the message from the first choice in the list of choices.

        Returns:
        -------
        str
            The content of the message from the first choice.
        """
        return self.choices[0].get('message').get('content')



from abc import ABC


class JsonSerialize(ABC):
    """
    This class provides methods to serialize objects to and from JSON format.

    Attributes:
        None

    Methods:
        from_json(cls, json: dict) -> Any: Creates a new instance of the child class from a JSON response returned by the OpenAI API.
        to_json(self) -> dict: Serializes an instance of the class to a dictionary in JSON format.
    """

    @classmethod
    def from_json(cls, json: dict) -> any:
        """
        Creates a new instance of the child class from a JSON response returned by the OpenAI API.

        Args:
            json (dict): A JSON response returned by the OpenAI API.

        Returns:
            Any: A new instance of the child class.
        """
        instance = cls(**json)
        return instance

    def to_json(self) -> dict:
        """
        Serializes an instance of the class to a dictionary in JSON format.

        Args:
            None

        Returns:
            dict: A dictionary containing the serialized instance data in JSON format.
        """
        return vars(self)

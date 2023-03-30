class CompletionResponse:
    """Class representing a response to a completion request."""

    def __init__(self, *, choices: list[dict], created: int, id: str, model: str, object: str, usage: dict):
        """Initialize a new CompletionResponse object.

        Parameters:
            choices: A list of choices for the completion request, where each choice is a dictionary.
            created: The UNIX timestamp indicating when the completion request was created.
            id: A string identifying the completion request.
            model: The name of the model used for the completion request.
            object: The object for which the completion request was made.
            usage: A dictionary containing usage statistics for the completion request.
        """
        self.choices: list[dict] = choices
        self.created: int = created
        self._id: str = id
        self.model: str = model
        self.object: str = object
        self.usage: dict = usage

    @property
    def text(self) -> str | None:
        return self.choices[0].get('text')

    @classmethod
    def from_json(cls, json: dict[str]):
        return cls(**json)

    def to_json(self) -> dict:
        return vars(self)

    def __repr__(self) -> str:
        return f'CompletionResponse(id={self._id}, text={self.text})'

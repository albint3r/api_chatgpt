import openai
from config import APIConfiguration
from domain.completion.completion_response import CompletionResponse
from domain.completion.i_completion_facade import ICompletionFacade
from injector import inject


class CompletionFacadeImpl(ICompletionFacade):
    """Class representing a facade for creating completion requests."""
    @inject
    def __init__(self, config: APIConfiguration):
        """Initialize a new CompletionFacadeImpl object.

        Parameters:
        config: An APIConfiguration object containing the configuration for the OpenAI API.
        """
        self.config: APIConfiguration = config

    def create(self, *, prompt: str) -> CompletionResponse:
        """Create a new completion request and return the response.

        Parameters:
        prompt: A string containing the prompt for the completion request.

        Returns:
            A CompletionResponse object representing the response to the completion request.
        """
        openai.api_key = self.config.api_key
        response = openai.Completion.create(model=self.config.api_model,
                                            prompt=prompt,
                                            temperature=self.config.api_temperature,
                                            max_tokens=50)

        return CompletionResponse.from_json(response)

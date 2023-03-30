import openai
from config import APIConfiguration
from domain.completion.i_completion_facade import ICompletionFacade
from injector import inject


class CompletionFacadeImpl(ICompletionFacade):
    @inject
    def __init__(self, config: APIConfiguration):
        self.config: APIConfiguration = config

    def create(self, *, prompt: str) -> dict[str]:
        openai.api_key = self.config.api_key
        return openai.Completion.create(model=self.config.api_model,
                                            prompt=prompt,
                                            temperature=self.config.api_temperature,
                                            max_tokens=50)

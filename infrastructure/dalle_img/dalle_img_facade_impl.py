import openai
from injector import inject

from config import APIConfiguration
from domain.dalle_img.i_dalle_img_facade import IDalleImgFacade
from domain.dalle_img.img_response import ImgResponse


class DalleImgFacadeImpl(IDalleImgFacade):
    """Class representing a facade for creating DALL-E image requests."""

    @inject
    def __init__(self, config: APIConfiguration):
        """Initialize a new DalleImgFacadeImpl object.

        Parameters:
        config: An APIConfiguration object containing the configuration for the OpenAI API.
        """
        self.config: APIConfiguration = config

    def run(self, *, size: str = '512x512') -> ImgResponse:
        """Create a new DALL-E image request and return the response.

        Parameters:
        prompt: A string containing the prompt for the DALL-E image request.
        size: An optional string containing the size of the output image. Defaults to '512x512'.

        Returns:
            An ImgResponse object representing the response to the DALL-E image request.
        """
        openai.api_key = self.config.api_key
        print('Dalle Image Creator:')
        print('-' * 100)
        user_input = input('>:')
        print('wait response...')
        response = openai.Image.create(prompt=user_input, n=1, size=size)
        print(response)
        return ImgResponse.from_json(response)

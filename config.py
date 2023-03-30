from dotenv import dotenv_values


class APIConfiguration:

    def __init__(self):
        self._env: dict[str, str | None] = dotenv_values(".env")

    @property
    def api_key(self) -> str:
        return self._env.get('OPEN_AI_TOKEN')

    @property
    def api_model(self) -> str:
        return self._env.get('MODEL')

    @property
    def api_temperature(self) -> float:
        return float(self._env.get('TEMPERATURE'))

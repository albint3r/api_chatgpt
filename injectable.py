from injector import Module, provider

from config import APIConfiguration


class AppModule(Module):
    @provider
    def provide_config(self) -> APIConfiguration:
        return APIConfiguration()

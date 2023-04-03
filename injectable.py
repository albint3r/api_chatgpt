from injector import Module, provider

from config import APIConfiguration
from infrastructure.message_classifier.topic_predictor_facade_impl import MessageClassifierFacade


class AppModule(Module):
    @provider
    def provide_config(self) -> APIConfiguration:
        return APIConfiguration()

    @provider
    def provide_i_topic_predictor_facade(self) -> MessageClassifierFacade:
        return MessageClassifierFacade()

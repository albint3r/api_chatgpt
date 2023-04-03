from transformers import Pipeline, pipeline

from config import APIConfiguration
from domain.chat_bot.message import Message
from domain.message_classifier.i_message_classifier_facade import IMessageClassifierFacade


class MessageClassifierFacade(IMessageClassifierFacade):

    def __init__(self):
        self.classifier: Pipeline | None = None
        self.config: APIConfiguration | None = None

    def initialize(self, config: APIConfiguration) -> None:
        self.config = config
        task: str = "zero-shot-classification"
        model: str = "Recognai/bert-base-spanish-wwm-cased-xnli"
        self.classifier = pipeline(task, model=model)

    def predict(self, msg: Message) -> Pipeline:
        return self.classifier(msg.content,
                               candidate_labels=["servicio", "informacion", "otro"], )

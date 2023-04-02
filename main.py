from injector import Injector

from infrastructure.chat_bot.chat_bot_facade_impl import ChatBotFacade
from infrastructure.dalle_img.dalle_img_facade_impl import DalleImgFacadeImpl
from injectable import AppModule

injector = Injector(AppModule())


def main_chat() -> None:
    facade = injector.get(ChatBotFacade)
    facade.run()


def main_img() -> None:
    facade = injector.get(DalleImgFacadeImpl)
    facade.run()


if __name__ == '__main__':
    main_chat()

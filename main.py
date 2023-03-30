from injector import Injector
# from infrastructure.completion.completion_facade_impl import CompletionFacadeImpl
from infrastructure.dalle_img.dalle_img_facade_impl import DalleImgFacadeImpl
from injectable import AppModule

injector = Injector(AppModule())


def main() -> None:
    facade = injector.get(DalleImgFacadeImpl)
    print(facade.create(prompt="beautiful house with red seal"))


if __name__ == '__main__':
    main()

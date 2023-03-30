from injector import Injector
from infrastructure.completion.completion_facade_impl import CompletionFacadeImpl
from injectable import AppModule

injector = Injector(AppModule())


def main():
    facade = injector.get(CompletionFacadeImpl)
    print(facade.create(prompt='Cuentame un cuento de adas'))


if __name__ == '__main__':
    main()

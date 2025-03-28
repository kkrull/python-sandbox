from abc import abstractmethod
from typing import Callable, Generic, NewType, Protocol, TypeVar, Union

StringList = NewType("StringList", list[str])

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


type Either[A, B] = Union[Left[A, B], Right[A, B]]


class EitherBase[A, B]:
    @abstractmethod
    def flatMap(self, fn: Callable[[B], Either[A, C]]) -> Either[A, C]:
        pass

    @abstractmethod
    def getOrElse(self, fallbackValue: B) -> B:
        pass

    @abstractmethod
    def map(self, _fn: Callable[[B], C]) -> Either[A, C]:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Left[A, B](EitherBase[A, B]):
    def __init__(self, value: A):
        self.__value = value

    def flatMap(self, _fn: Callable[[B], Either[A, C]]) -> Either[A, C]:
        return Left[A, C](self.__value)

    def getOrElse(self, fallbackValue: B) -> B:
        return fallbackValue

    def map(self, _fn: Callable[[B], C]) -> Either[A, C]:
        return Left[A, C](self.__value)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Left({self.__value})"


class Right[A, B](EitherBase[A, B]):
    def __init__(self, value: B):
        self.__value = value

    def flatMap(self, fn: Callable[[B], Either[A, C]]) -> Either[A, C]:
        return fn(self.__value)

    def getOrElse(self, _fallbackValue: B) -> B:
        return self.__value

    def map(self, fn: Callable[[B], C]) -> Either[A, C]:
        return Right(fn(self.__value))

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Right({self.__value})"

from abc import abstractmethod
from typing import Callable, TypeVar, Union, override

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


type Either[A, B] = Union[Left[A, B], Right[A, B]]


class EitherBase[A, B]:
    """
    An immutable container of either a left-hand value of type Left[A] or a right-hand value of type
    Right[B].

    Left-hand values are typically used for errors or lack of ability to proceed further with an
    algorithm. Mapping functions are right-associative.  In other words, mapping functions are
    applied to right-hand values, but left-hand values are returned as-is.
    """

    @abstractmethod
    def flat_map(self, fn: Callable[[B], Either[A, C]]) -> Either[A, C]:
        """Replace Right with the result of calling the given function, or return Left unchanged."""
        pass

    @abstractmethod
    def get_or_else(self, fallback_value: B) -> B:
        """Get Right's inner value, or-in the case of Left-the given fallback value."""
        pass

    @property
    @abstractmethod
    def is_left(self) -> bool:
        """True if this is Left; False if Right"""
        pass

    @property
    @abstractmethod
    def is_right(self) -> bool:
        """True if this is Right; False if Left"""
        pass

    @property
    @abstractmethod
    def left_value(self) -> A:
        """Return the wrapped Left value or throw if Right"""
        pass

    @abstractmethod
    def map(self, fn: Callable[[B], C]) -> Either[A, C]:
        """Transform Right's inner value with the given function, or return Left unchanged."""
        pass

    # TODO KDK: Revisit these https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr/1436756#1436756
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Left[A, B](EitherBase[A, B]):
    __match_args__ = ("_value",)

    def __init__(self, value: A):
        self._value = value

    @override
    def flat_map(self, _fn: Callable[[B], Either[A, C]]) -> Either[A, C]:
        return Left[A, C](self._value)

    @override
    def get_or_else(self, fallback_value: B) -> B:
        return fallback_value

    @property
    @override
    def is_left(self) -> bool:
        return True

    @property
    @override
    def is_right(self) -> bool:
        return False

    @property
    @override
    def left_value(self) -> A:
        return self._value

    @override
    def map(self, _fn: Callable[[B], C]) -> Either[A, C]:
        return Left[A, C](self._value)

    @override
    def __repr__(self) -> str:
        return f"Left({self._value})"

    @override
    def __str__(self) -> str:
        return f"Left({self._value})"


class Right[A, B](EitherBase[A, B]):
    __match_args__ = ("_value",)

    def __init__(self, value: B):
        self._value = value

    @override
    def flat_map(self, fn: Callable[[B], Either[A, C]]) -> Either[A, C]:
        return fn(self._value)

    @override
    def get_or_else(self, _fallback_value: B) -> B:
        return self._value

    @property
    @override
    def is_left(self) -> bool:
        return False

    @property
    @override
    def is_right(self) -> bool:
        return True

    @property
    @override
    def left_value(self) -> A:
        raise ValueError("Right has no left_value")

    @override
    def map(self, fn: Callable[[B], C]) -> Either[A, C]:
        return Right(fn(self._value))

    @override
    def __repr__(self) -> str:
        return f"Right({self._value})"

    @override
    def __str__(self) -> str:
        return f"Right({self._value})"

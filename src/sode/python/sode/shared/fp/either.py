from abc import abstractmethod
from typing import Callable, Tuple, TypeVar, Union, override

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


type Either[A, B] = Union[Left[A, B], Right[A, B]]

X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")


def flatten_3_or_left(
    x: Either[A, X],
    y: Either[A, Y],
    z: Either[A, Z],
) -> Either[A, Tuple[X, Y, Z]]:
    """Flatten to oen Right of the given sequence of right-hand values, or the first Left"""

    left_values = (e.left_value for e in (x, y, z) if e.is_left)
    match next(left_values, None):
        case None:
            right_values = (x.right_value, y.right_value, z.right_value)
            return Right(right_values)
        case first_left_value:
            return Left(first_left_value)


class EitherBase[A, B]:
    """
    An immutable container of either a left-hand value of type Left[A] or a right-hand value of type
    Right[B].

    Left-hand values are typically used for errors or lack of ability to proceed further with an
    algorithm. Mapping functions are right-associative.  In other words, mapping functions are
    applied to right-hand values, but left-hand values are returned as-is.
    """

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def do_try(
        self, exception_as_left: Callable[[Exception], A], risky_fn: Callable[[B], None]
    ) -> Either[A, B]:
        """
        Try calling an exception-prone risky_fn with Right's value, returning Right upon success.

        Return Left when Left invoked, or degrade to Left with the caught Exception (coerced back to
        the Left type with exception_as_left) if risky_fn raises any Exception.
        """
        pass

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

    @property
    @abstractmethod
    def right_value(self) -> B:
        """Return the wrapped Right value or throw if Left"""
        pass


class Left[A, B](EitherBase[A, B]):
    __match_args__ = ("_value",)

    def __init__(self, value: A):
        self._value = value

    @override
    def __repr__(self) -> str:
        return f"Left({self._value!r})"

    @override
    def __str__(self) -> str:
        return f"Left({self._value})"

    @override
    def do_try(
        self, _exception_as_left: Callable[[Exception], A], _fn: Callable[[B], None]
    ) -> Either[A, B]:
        return Left[A, B](self._value)

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

    @property
    @override
    def right_value(self) -> B:
        raise ValueError(f"{self!r} has no right hand value")


class Right[A, B](EitherBase[A, B]):
    __match_args__ = ("_value",)

    def __init__(self, value: B):
        self._value = value

    @override
    def __repr__(self) -> str:
        return f"Right({self._value!r})"

    @override
    def __str__(self) -> str:
        return f"Right({self._value})"

    @override
    def do_try(
        self, exception_as_left: Callable[[Exception], A], risky_fn: Callable[[B], None]
    ) -> Either[A, B]:
        try:
            risky_fn(self._value)
            return Right[A, B](self._value)
        except Exception as error:
            return Left[A, B](exception_as_left(error))

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

    @property
    @override
    def right_value(self) -> B:
        return self._value

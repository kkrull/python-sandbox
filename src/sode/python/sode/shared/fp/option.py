from abc import abstractmethod
from typing import Callable, TypeVar, Union, override

from .either import Either, Left, Right

A = TypeVar("A")
B = TypeVar("B")

type Option[A] = Union[Empty[A], Value[A]]


def new_option(maybe_value: A) -> Option[A]:
    """Return Empty if the given value is None, or Value with the given value otherwise."""

    if maybe_value is None:
        return Empty[A]()
    else:
        return Value[A](maybe_value)


class OptionBase[A]:
    """
    An immutable container that is either a Value of type A, or is Empty (e.g. a lack of value).
    Mapping functions apply to Value, but not to Empty.
    """

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def filter(self, predicate: Callable[[A], bool]) -> Option[A]:
        """Remain a Value if the given predicate returns True; be Empty otherwise."""
        pass

    @abstractmethod
    def flat_map(self, fn: Callable[[A], Option[B]]) -> Option[B]:
        """Replace Value with the1 result of the given function, or return Empty unchanged."""
        pass

    @abstractmethod
    def get_or_else(self, fallback_value: A) -> A:
        """Get Value's inner value, or-in the case of Empty-the given fallback value."""
        pass

    @property
    @abstractmethod
    def is_present(self) -> bool:
        pass

    @abstractmethod
    def map(self, fn: Callable[[A], B]) -> Option[B]:
        """Transform Value with the result of the given function, or return Empty unchanged."""
        pass

    @abstractmethod
    def to_right[L](self, left_value: L) -> Either[L, A]:
        """Convert a Value to Right or Empty to Left with the given left-hand (e.g. error) value."""
        pass


class Empty[A](OptionBase[A]):
    """An empty container, lacking a value"""

    @override
    def __repr__(self) -> str:
        return f"Empty()"

    @override
    def __str__(self) -> str:
        return f"Empty"

    @override
    def filter(self, _predicate: Callable[[A], bool]) -> Option[A]:
        return Empty[A]()

    @override
    def flat_map(self, _fn: Callable[[A], Option[B]]) -> Option[B]:
        return Empty[B]()

    @override
    def get_or_else(self, fallback_value: A) -> A:
        return fallback_value

    @property
    @override
    def is_present(self) -> bool:
        return False

    @override
    def map(self, _fn: Callable[[A], B]) -> Option[B]:
        return Empty[B]()

    @override
    def to_right[L](self, left_value: L) -> Either[L, A]:
        return Left[L, A](left_value)


class Value[A](OptionBase[A]):
    """A container with a value inside"""

    __match_args__ = ("_value",)

    def __init__(self, value: A):
        self._value = value

    @override
    def __repr__(self) -> str:
        return f"Value({self._value!r})"

    @override
    def __str__(self) -> str:
        return f"Value({self._value})"

    @override
    def filter(self, predicate: Callable[[A], bool]) -> Option[A]:
        if predicate(self._value):
            return self
        else:
            return Empty[A]()

    @override
    def flat_map(self, fn: Callable[[A], Option[B]]) -> Option[B]:
        return fn(self._value)

    @override
    def get_or_else(self, _fallback_value: A) -> A:
        return self._value

    @property
    @override
    def is_present(self) -> bool:
        return True

    @override
    def map(self, fn: Callable[[A], B]) -> Option[B]:
        return Value[B](fn(self._value))

    @override
    def to_right[L](self, _left_value: L) -> Either[L, A]:
        return Right[L, A](self._value)

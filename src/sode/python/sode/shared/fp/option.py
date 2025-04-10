from abc import abstractmethod
from typing import Callable, TypeVar, Union, override

from .either import Either, Left, Right

A = TypeVar("A")
B = TypeVar("B")

type Option[A] = Union[Empty[A], Value[A]]


def new_option(maybe_value: A) -> Option[A]:
    """Return Empty if the given value is None, or Value with the given value otherwise."""
    if maybe_value is None:
        return Empty()
    else:
        return Value(maybe_value)


class OptionBase[A]:
    """
    An immutable container that is either a Value of type A, or is Empty (e.g. a lack of value).

    Mapping functions apply to Value, but not to Empty.
    """

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
    def to_right(self, left_value: B) -> Either[B, A]:
        """Get Value's inner value, or-in the case of Empty-the given fallback value."""
        pass


class Empty[A](OptionBase[A]):
    """An empty container, lacking a value"""

    @override
    def __repr__(self) -> str:
        return f"Empty"

    @override
    def filter(self, _predicate: Callable[[A], bool]) -> Option[A]:
        return Empty[A]()

    @override
    def flat_map(self, _fn: Callable[[A], Option[B]]) -> Option[B]:
        return Empty()

    @override
    def get_or_else(self, fallback_value: A) -> A:
        return fallback_value

    @property
    @override
    def is_present(self) -> bool:
        return False

    @override
    def map(self, _fn: Callable[[A], B]) -> Option[B]:
        return Empty()

    @override
    def to_right(self, left_value: B) -> Either[B, A]:
        return Left(left_value)


class Value[A](OptionBase[A]):
    """A container with a value inside"""

    __match_args__ = ("value",)

    def __init__(self, value: A):
        self.value = value

    @override
    def __repr__(self) -> str:
        return f"Value({self.value})"

    @override
    def filter(self, predicate: Callable[[A], bool]) -> Option[A]:
        if predicate(self.value):
            return self
        else:
            return Empty[A]()

    @override
    def flat_map(self, fn: Callable[[A], Option[B]]) -> Option[B]:
        return fn(self.value)

    @override
    def get_or_else(self, _fallback_value: A) -> A:
        return self.value

    @property
    @override
    def is_present(self) -> bool:
        return True

    @override
    def map(self, fn: Callable[[A], B]) -> Option[B]:
        return Value(fn(self.value))

    @override
    def to_right(self, _left_value: B) -> Either[B, A]:
        return Right(self.value)

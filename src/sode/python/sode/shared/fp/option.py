from abc import abstractmethod
from typing import Callable, TypeVar, Union, override

A = TypeVar("A")
B = TypeVar("B")

type Option[A] = Union[Empty[A], Value[A]]


class OptionBase[A]:
    """
    An immutable container that is either a Value of type A, or is Empty (e.g. a lack of value).

    Mapping functions apply to Value, but not to Empty.
    """

    @abstractmethod
    def flat_map(self, fn: Callable[[A], Option[B]]) -> Option[B]:
        """Replace Value with the1 result of the given function, or return Empty unchanged."""
        pass

    @abstractmethod
    def get_or_else(self, fallbackValue: A) -> A:
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


class Empty[A](OptionBase[A]):
    """An empty container, lacking a value"""

    @override
    def __repr__(self) -> str:
        return f"Empty"

    @override
    def flat_map(self, fn: Callable[[A], Option[B]]) -> Option[B]:
        return Empty()

    @override
    def get_or_else(self, fallbackValue: A) -> A:
        return fallbackValue

    @property
    def is_present(self) -> bool:
        return False

    @override
    def map(self, fn: Callable[[A], B]) -> Option[B]:
        return Empty()


class Value[A](OptionBase[A]):
    """A container with a value inside"""

    __match_args__ = ("value",)

    def __init__(self, value: A):
        self.value = value

    @override
    def __repr__(self) -> str:
        return f"Value({self.value})"

    @override
    def flat_map(self, fn: Callable[[A], Option[B]]) -> Option[B]:
        return fn(self.value)

    @override
    def get_or_else(self, fallbackValue: A) -> A:
        return self.value

    @property
    def is_present(self) -> bool:
        return True

    @override
    def map(self, fn: Callable[[A], B]) -> Option[B]:
        return Value(fn(self.value))

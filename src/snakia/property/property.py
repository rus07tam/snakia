from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

from snakia.types import empty

T = TypeVar("T")


class Property(Generic[T]):
    """
    A property that can be set, get, and deleted.
    """

    __slots__ = "__fget", "__fset", "__fdel", "__name"

    __name: str

    def __init__(
        self,
        fget: Callable[[Any], T] = empty.func,
        fset: Callable[[Any, T], None] = empty.func,
        fdel: Callable[[Any], None] = empty.func,
    ) -> None:
        self.__fget = fget
        self.__fset = fset
        self.__fdel = fdel

    def __set_name__(self, owner: type, name: str) -> None:
        self.__name = name

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        return self.__fget(instance)

    def __set__(self, instance: Any, value: T, /) -> None:
        return self.__fset(instance, value)

    def __delete__(self, instance: Any, /) -> None:
        return self.__fdel(instance)

    def getter(self, fget: Callable[[Any], T], /) -> Property[T]:
        """Descriptor getter."""
        self.__fget = fget
        return self

    def setter(self, fset: Callable[[Any, T], None], /) -> Property[T]:
        """Descriptor setter."""
        self.__fset = fset
        return self

    def deleter(self, fdel: Callable[[Any], None], /) -> Property[T]:
        """Descriptor deleter."""
        self.__fdel = fdel
        return self

    @property
    def name(self) -> str:
        return self.__name

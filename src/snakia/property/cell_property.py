from __future__ import annotations

from typing import Any, Generic, Protocol, TypeAlias, TypeVar

from typing_extensions import Self

from snakia.types import empty

T = TypeVar("T")

_Cell: TypeAlias = T | None


class _Getter(Protocol, Generic[T]):
    def __call__(self, instance: Any, cell: _Cell[T], /) -> T: ...


class _Setter(Protocol, Generic[T]):
    def __call__(self, instance: Any, cell: _Cell[T], value: T, /) -> _Cell[T]: ...


class _Deleter(Protocol, Generic[T]):
    def __call__(self, instance: Any, cell: _Cell[T], /) -> _Cell[T]: ...


class CellProperty(Generic[T]):
    """
    A property that uses a cell to store its value.
    """

    __slots__ = ("__name", "__fget", "__fset", "__fdel")

    def __init__(
        self,
        fget: _Getter[T],
        fset: _Setter[T] = empty.func,
        fdel: _Deleter[T] = empty.func,
    ) -> None:
        self.__fget: _Getter[T] = fget
        self.__fset: _Setter[T] = fset
        self.__fdel: _Deleter[T] = fdel
        self.__name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.__name = f"_{owner.__name__}__{name}"

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        cell = self.__fget(instance, self.__get_cell(instance))
        self.__set_cell(instance, cell)
        return cell

    def __set__(self, instance: Any, value: T, /) -> None:
        cell = self.__fset(instance, self.__get_cell(instance), value)
        self.__set_cell(instance, cell)

    def __delete__(self, instance: Any, /) -> None:
        cell = self.__fdel(instance, self.__get_cell(instance))
        self.__set_cell(instance, cell)

    def getter(self, fget: _Getter[T], /) -> Self:
        """Descriptor getter."""
        self.__fget = fget
        return self

    def setter(self, fset: _Setter[T], /) -> Self:
        """Descriptor setter."""
        self.__fset = fset
        return self

    def deleter(self, fdel: _Deleter[T], /) -> Self:
        """Descriptor deleter."""
        self.__fdel = fdel
        return self

    def __get_cell(self, instance: Any) -> T | None:
        return getattr(instance, self.__name, None)

    def __set_cell(self, instance: Any, value: T | None) -> None:
        if value is None:
            delattr(instance, self.__name)
        else:
            setattr(instance, self.__name, value)

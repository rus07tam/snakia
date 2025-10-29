from typing import TypeVar

T = TypeVar("T")


def singleton(cls: type[T]) -> T:
    return cls()

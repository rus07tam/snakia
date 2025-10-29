from typing import Callable, TypeVar

T = TypeVar("T")


def const(value: T) -> Callable[[], T]:
    return lambda: value

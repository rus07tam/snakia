from typing import Any, Callable, TypeVar

T = TypeVar("T")


def side(value: T, *_: Any, **__: Any) -> T:
    return value


def side_func(value: T, *_: Any, **__: Any) -> Callable[..., T]:
    return lambda *_, **__: value

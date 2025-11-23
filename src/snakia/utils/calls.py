from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def call(f: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return f(*args, **kwargs)


def caller(f: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> Callable[..., T]:
    return lambda *_, **__: f(*args, **kwargs)

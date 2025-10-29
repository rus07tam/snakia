from typing import Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def to_async(func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    """Convert a sync function to an async function."""

    async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return inner

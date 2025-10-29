import builtins
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


# noqa: W0622 # pylint: disable=W0622
def map(func: Callable[[T], U], /) -> Callable[[Iterable[T]], Iterable[U]]:
    return lambda iterable: builtins.map(func, iterable)

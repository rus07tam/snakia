import builtins
from typing import Callable, Iterable, TypeGuard, TypeVar

S = TypeVar("S")
T = TypeVar("T")


# noqa: W0622 # pylint: disable=W0622
def filter(
    f: Callable[[S], TypeGuard[T]],
) -> Callable[[Iterable[S]], Iterable[T]]:
    return lambda iterable: builtins.filter(f, iterable)

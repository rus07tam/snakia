import builtins
from typing import Callable, Iterable, TypeGuard


# noqa: W0622 # pylint: disable=W0622
def filter[S, T](
    f: Callable[[S], TypeGuard[T]],
) -> Callable[[Iterable[S]], Iterable[T]]:
    return lambda iterable: builtins.filter(f, iterable)

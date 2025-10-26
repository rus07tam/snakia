import builtins
from typing import Any, Callable, Iterable


# noqa: W0622 # pylint: disable=W0622
def map[T: Any, U](
    func: Callable[[T], U], /
) -> Callable[[Iterable[T]], Iterable[U]]:
    return lambda iterable: builtins.map(func, iterable)

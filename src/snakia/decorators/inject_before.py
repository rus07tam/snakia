from typing import Any, Callable, ParamSpec, TypeVar

from .inject_replace import inject_replace

P = ParamSpec("P")
T = TypeVar("T")
R = TypeVar("R")


def inject_before(obj: T, target: Callable[P, R], hook: Callable[P, Any]) -> T:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        hook(*args, **kwargs)
        return target(*args, **kwargs)

    return inject_replace(obj, target, inner)


def before_hook(
    obj: object, target: Callable[P, R]
) -> Callable[[Callable[P, Any]], Callable[P, Any]]:

    def hook(new: Callable[P, Any]) -> Callable[P, Any]:
        inject_before(obj, target, new)
        return new

    return hook

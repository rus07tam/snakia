from typing import Callable, ParamSpec, TypeVar

from .inject_replace import inject_replace

P = ParamSpec("P")
T = TypeVar("T")
R = TypeVar("R")


def inject_after(obj: T, target: Callable[P, R], hook: Callable[[R], R]) -> T:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return hook(target(*args, **kwargs))

    return inject_replace(obj, target, inner)


def after_hook(
    obj: object, target: Callable[P, R]
) -> Callable[[Callable[[R], R]], Callable[[R], R]]:
    def hook(new: Callable[[R], R]) -> Callable[[R], R]:
        inject_after(obj, target, new)
        return new

    return hook

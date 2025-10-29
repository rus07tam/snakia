from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")
F = TypeVar("F")


def cond(
    condition: Callable[P, bool],
    if_true: Callable[P, T],
    if_false: Callable[P, F],
) -> Callable[P, T | F]:
    return lambda *args, **kw: (
        if_true(*args, **kw) if condition(*args, **kw) else if_false(*args, **kw)
    )

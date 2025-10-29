from typing import Any, Callable, ParamSpec

P = ParamSpec("P")


def concat(*funcs: Callable[P, Any]) -> Callable[P, None]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> None:
        for f in funcs:
            f(*args, **kwargs)

    return inner

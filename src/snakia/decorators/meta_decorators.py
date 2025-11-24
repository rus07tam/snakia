import functools
from typing import Callable, Concatenate, ParamSpec, TypeVar

T = TypeVar("T")
R = TypeVar("R")
D = ParamSpec("D")
P = ParamSpec("P")


def inject_decorator(
    decorator: Callable[Concatenate[Callable[P, T], D], None],
) -> Callable[D, Callable[[Callable[P, T]], Callable[P, T]]]:

    @functools.wraps(decorator)
    def wrapper(
        *d_args: D.args, **d_kwargs: D.kwargs
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        def inner(obj: Callable[P, T]) -> Callable[P, T]:
            @functools.wraps(obj)
            def func(*args: P.args, **kwargs: P.kwargs) -> T:
                decorator(obj, *d_args, **d_kwargs)
                return obj(*args, **kwargs)

            return func

        return inner

    return wrapper


def hook_decorator(
    decorator: Callable[Concatenate[Callable[P, T], T, D], T],
) -> Callable[D, Callable[[Callable[P, T]], Callable[P, T]]]:

    @functools.wraps(decorator)
    def wrapper(
        *d_args: D.args, **d_kwargs: D.kwargs
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        def inner(obj: Callable[P, T]) -> Callable[P, T]:
            @functools.wraps(obj)
            def func(*args: P.args, **kwargs: P.kwargs) -> T:
                val = obj(*args, **kwargs)
                return decorator(obj, val, *d_args, **d_kwargs)

            return func

        return inner

    return wrapper


def replace_decorator(
    decorator: Callable[Concatenate[T, D], T],
) -> Callable[D, Callable[[T], T]]:
    @functools.wraps(decorator)
    def wrapper(*d_args: D.args, **d_kwargs: D.kwargs) -> Callable[[T], T]:
        def inner(obj: T) -> T:
            result = decorator(obj, *d_args, **d_kwargs)
            if not callable(obj):
                return result
            for attr in functools.WRAPPER_ASSIGNMENTS:
                try:
                    value = getattr(obj, attr)
                except AttributeError:
                    pass
                else:
                    setattr(result, attr, value)
            return result

        return inner

    return wrapper

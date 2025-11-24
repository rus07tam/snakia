from typing import Any, Awaitable, Callable, ParamSpec, TypeVar, overload

P = ParamSpec("P")

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")


@overload
def chain(func1: Callable[P, A], /) -> Callable[P, A]: ...


@overload
def chain(
    func1: Callable[P, A], func2: Callable[[A], B], /
) -> Callable[P, B]: ...
@overload
def chain(
    func1: Callable[P, A], func2: Callable[[A], B], func3: Callable[[B], C], /
) -> Callable[P, C]: ...
@overload
def chain(
    func1: Callable[P, A],
    func2: Callable[[A], B],
    func3: Callable[[B], C],
    func4: Callable[[C], D],
    /,
) -> Callable[P, D]: ...


@overload
def chain(
    func1: Callable[P, A],
    func2: Callable[[A], B],
    func3: Callable[[B], C],
    func4: Callable[[C], D],
    func5: Callable[[D], E],
    /,
) -> Callable[P, E]: ...


@overload
def chain(
    func1: Callable[P, Any], /, *funcs: Callable[[Any], Any]
) -> Callable[P, Any]: ...


def chain(
    func1: Callable[P, Any], /, *funcs: Callable[[Any], Any]
) -> Callable[P, Any]:

    def inner(*args: P.args, **kwargs: P.kwargs) -> Any:
        v = func1(*args, **kwargs)
        for f in funcs:
            v = f(v)
        return v

    return inner


@overload
def async_chain(
    func1: Callable[P, Awaitable[A]], /
) -> Callable[P, Awaitable[A]]: ...


@overload
def async_chain(
    func1: Callable[P, Awaitable[A]], func2: Callable[[A], Awaitable[B]], /
) -> Callable[P, Awaitable[B]]: ...


@overload
def async_chain(
    func1: Callable[P, Awaitable[A]],
    func2: Callable[[A], Awaitable[B]],
    func3: Callable[[B], Awaitable[C]],
    /,
) -> Callable[P, Awaitable[C]]: ...


@overload
def async_chain(
    func1: Callable[P, Awaitable[A]],
    func2: Callable[[A], Awaitable[B]],
    func3: Callable[[B], Awaitable[C]],
    func4: Callable[[C], Awaitable[D]],
    /,
) -> Callable[P, Awaitable[D]]: ...


@overload
def async_chain(
    func1: Callable[P, Awaitable[A]],
    func2: Callable[[A], Awaitable[B]],
    func3: Callable[[B], Awaitable[C]],
    func4: Callable[[C], Awaitable[D]],
    func5: Callable[[D], Awaitable[E]],
    /,
) -> Callable[P, Awaitable[E]]: ...


@overload
def async_chain(
    func1: Callable[P, Any], /, *funcs: Callable[[Any], Awaitable[Any]]
) -> Callable[P, Awaitable[Any]]: ...


def async_chain(
    func1: Callable[P, Awaitable[Any]],
    /,
    *funcs: Callable[[Any], Awaitable[Any]],
) -> Callable[P, Awaitable[Any]]:

    async def inner(*args: P.args, **kwargs: P.kwargs) -> Any:
        v = await func1(*args, **kwargs)
        for f in funcs:
            v = await f(v)
        return v

    return inner

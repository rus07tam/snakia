import contextlib
from typing import Any, Callable, NoReturn, TypeVar, overload

from exceptiongroup import ExceptionGroup

from snakia.types.unset import Unset

E = TypeVar("E", bound=Exception)
T = TypeVar("T")
D = TypeVar("D")


@overload
def throw(
    *exceptions: E,  # pyright: ignore[reportInvalidTypeVarUse]
    from_: Unset | BaseException = Unset(),
) -> NoReturn: ...


@overload
def throw(
    exception: BaseException, from_: Unset | BaseException = Unset(), /
) -> NoReturn: ...


def throw(*exceptions: Any, from_: Unset | BaseException = Unset()) -> NoReturn:
    """Throw an exception."""
    if isinstance(from_, Unset):
        if len(exceptions) == 1:
            raise exceptions[0]
        raise ExceptionGroup("", exceptions)
    if len(exceptions) == 1:
        raise exceptions[0] from from_
    raise ExceptionGroup("", exceptions) from from_


contextlib.suppress()


@overload
def catch(
    func: Callable[[], T],
    *exceptions: type[Exception] | type[BaseException],
    default: None = None,
) -> T | None: ...
@overload
def catch(
    func: Callable[[], T],
    *exceptions: type[Exception] | type[BaseException],
    default: D,
) -> T | D: ...
def catch(
    func: Callable[[], T],
    *exceptions: type[Exception] | type[BaseException],
    default: Any = None,
) -> T | Any:
    try:
        return func()
    except BaseException as e:
        if any(isinstance(e, exc) for exc in exceptions):
            return default
        raise

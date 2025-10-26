from typing import Any, final


def func(*_: Any, **__: Any) -> Any:
    """
    A function that does nothing
    """


async def async_func(*_: Any, **__: Any) -> Any:
    """
    An async function that does nothing
    """


@final
class Class:  # noqa: R0903 # pylint: disable=R0903
    """
    A class that does nothing
    """

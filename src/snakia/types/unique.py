from typing import Any, TypeVar, final

T = TypeVar("T")


@final
class UniqueType(type):
    """
    A metaclass that prevents multiple instances of a class from being created.
    """

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwds: Any,
    ) -> type:
        t = super().__new__(mcs, name, bases, {})
        setattr(t, "__new__", lambda cls, *args, **kwargs: cls)
        return t

    @final
    def __init__(
        cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> None:
        super().__init__(name, bases, namespace)

    def __instancecheck__(cls, instance: Any) -> bool:
        return instance is cls

    def __eq__(cls, other: Any) -> bool:
        return cls is other

    def __call__(cls: type[T]) -> T:
        return cls.__new__(cls)  # noqa: E1120 # pylint: disable=E1120


class Unique(metaclass=UniqueType):  # noqa: R0903 # pylint: disable=R0903
    """
    A class that prevents multiple instances of a class from being created.
    """


def unique(name: str) -> UniqueType:
    """Factory for creating a unique type."""
    return UniqueType(name, (), {})

from typing import Any, Callable, Final, Generic, TypeVar, overload
from typing_extensions import Self

T = TypeVar("T")


class PrivProperty(Generic[T]):
    __slots__ = "__name", "__default_value", "__default_factory"

    __name: str

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, default_value: T) -> None: ...
    @overload
    def __init__(self, *, default_factory: Callable[[Self], T]) -> None: ...
    def __init__(
        self,
        default_value: T | None = None,
        default_factory: Callable[[Self], T] | None = None,
    ) -> None:
        self.__default_value: Final[T | None] = default_value
        self.__default_factory: Final[Callable[[Self], T] | None] = (
            default_factory
        )

    def _get_default(self: Self) -> T:
        if self.__default_value is not None:
            return self.__default_value
        if self.__default_factory is not None:
            return self.__default_factory(self)
        raise ValueError("Either default_value or default_factory must be set")

    def __set_name__(self, owner: type, name: str) -> None:
        self.__name = f"_{owner.__name__}__{name}"

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        if not hasattr(instance, self.__name):
            setattr(instance, self.__name, self._get_default())
        return getattr(instance, self.__name)  # type: ignore

    def __set__(self, instance: Any, value: T, /) -> None:
        setattr(instance, self.__name, value)

    def __delete__(self, instance: Any, /) -> None:
        delattr(instance, self.__name)

    @property
    def name(self) -> str:
        """Return the name of the variable associated with the property."""
        return self.__name

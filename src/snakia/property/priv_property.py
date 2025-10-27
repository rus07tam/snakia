from typing import Any


class PrivProperty[T]:
    __slots__ = "__name", "__default_value"

    __name: str

    def __init__(self, default_value: T | None = None) -> None:
        self.__default_value: T | None = default_value

    def __set_name__(self, owner: type, name: str) -> None:
        self.__name = f"_{owner.__name__}__{name}"

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        if self.__default_value:
            return getattr(instance, self.__name, self.__default_value)
        return getattr(instance, self.__name)  # type: ignore

    def __set__(self, instance: Any, value: T, /) -> None:
        setattr(instance, self.__name, value)

    def __delete__(self, instance: Any, /) -> None:
        delattr(instance, self.__name)

    @property
    def name(self) -> str:
        """Return the name of the variable associated with the property."""
        return self.__name

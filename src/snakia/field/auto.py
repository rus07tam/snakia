import pickle
from typing import Callable, Final, Generic, TypeVar, overload

from typing_extensions import Self

from .field import Field

T = TypeVar("T")


class AutoField(Field[T], Generic[T]):
    __slots__ = ("__target_type",)

    @overload
    def __init__(
        self, default_value: T, *, target_type: type[T] | None = None
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        default_factory: Callable[[Self], T],
        target_type: type[T] | None = None,
    ) -> None: ...
    def __init__(
        self,
        default_value: T | None = None,
        *,
        default_factory: Callable[[Self], T] | None = None,
        target_type: type[T] | None = None,
    ) -> None:
        if default_factory is not None and default_value is None:
            super().__init__(default_factory=default_factory)
        elif default_value is not None and default_factory is None:
            super().__init__(default_value)
        self.__target_type: Final = target_type

    def serialize(self, value: T, /) -> bytes:
        return pickle.dumps(value)

    def deserialize(self, serialized: bytes, /) -> T:
        value = pickle.loads(serialized)
        if not isinstance(value, self.__target_type or object):
            return self._get_default()
        return value  # type: ignore

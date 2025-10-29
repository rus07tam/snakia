import pickle
from typing import Final, Generic, TypeVar

from .field import Field

T = TypeVar("T")


class AutoField(Field[T], Generic[T]):
    __slots__ = ("__target_type",)

    def __init__(self, default_value: T, *, target_type: type[T] | None = None) -> None:
        super().__init__(default_value)
        self.__target_type: Final = target_type

    def serialize(self, value: T, /) -> bytes:
        return pickle.dumps(value)

    def deserialize(self, serialized: bytes, /) -> T:
        value = pickle.loads(serialized)
        if not isinstance(value, self.__target_type or object):
            return self.default_value
        return value  # type: ignore

import pickle
from typing import Final, override

from .field import Field


class AutoField[T](Field[T]):
    __slots__ = ("__target_type",)

    def __init__(
        self, default_value: T, *, target_type: type[T] | None = None
    ) -> None:
        super().__init__(default_value)
        self.__target_type: Final = target_type

    @override
    def serialize(self, value: T, /) -> bytes:
        return pickle.dumps(value)

    @override
    def deserialize(self, serialized: bytes, /) -> T:
        value = pickle.loads(serialized)
        if not isinstance(value, self.__target_type or object):
            return self.default_value
        return value  # type: ignore

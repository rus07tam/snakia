import struct

from .field import Field


class FloatField(Field[float]):
    def serialize(self, value: float, /) -> bytes:
        return struct.pack(">f", value)

    def deserialize(self, serialized: bytes, /) -> float:
        return struct.unpack(">f", serialized)[0]  # type: ignore

from .field import Field


class IntField(Field[int]):
    def serialize(self, value: int, /) -> bytes:
        length = (value.bit_length() + 7) // 8
        return value.to_bytes(length, "little")

    def deserialize(self, serialized: bytes, /) -> int:
        return int.from_bytes(serialized, "little")

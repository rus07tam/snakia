import os

from .random import Random


class OSRandom(Random[None]):
    """
    A random number generator that uses the OS (cryptographically secure) to generate random bytes.
    """

    def bits(self, k: int) -> int:
        v = os.urandom((k + 7) // 8)
        return int.from_bytes(v, "little") & ((1 << k) - 1)

    def get_state(self) -> None:
        return None

    def set_state(self, value: None) -> None:
        pass

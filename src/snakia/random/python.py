import random
from typing import TypeAlias

from .random import Random

_State: TypeAlias = tuple[int, tuple[int, ...], int | float | None]


class PythonRandom(Random[_State]):
    def bits(self, k: int) -> int:
        return random.getrandbits(k)

    def get_state(self) -> _State:
        return random.getstate()

    def set_state(self, value: _State) -> None:
        random.setstate(value)

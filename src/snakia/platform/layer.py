from __future__ import annotations

from typing import ClassVar, Generic, TypeVar, final, overload

from typing_extensions import Self

from .os import PlatformOS

T = TypeVar("T", bound=PlatformOS)


class PlatformLayer(Generic[T]):
    target: ClassVar[PlatformOS] = PlatformOS.UNKNOWN

    @final
    def __init__(self, platform: PlatformOS) -> None:
        if platform != self.target:
            raise NotImplementedError(
                f"{self.__class__.__name__} is not implemented for {platform._name_}"
            )

    @overload
    @classmethod
    def try_get(cls, platform: T, /) -> Self: ...
    @overload
    @classmethod
    def try_get(cls, platform: PlatformOS, /) -> Self | None: ...
    @classmethod
    def try_get(cls, platform: PlatformOS, /) -> Self | None:
        if platform == cls.target:
            return cls(platform)
        return None

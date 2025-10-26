from __future__ import annotations

import sys
from enum import IntEnum
from typing import Final


class PlatformOS(IntEnum):
    UNKNOWN = 0
    ANDROID = 1
    FREEBSD = 2
    IOS = 3
    LINUX = 4
    MACOS = 5
    WINDOWS = 6

    @property
    def is_apple(self) -> bool:
        """MacOS, iOS"""
        return self in [PlatformOS.MACOS, PlatformOS.IOS]

    @property
    def is_linux(self) -> bool:
        """Linux, Android"""
        return self in [PlatformOS.LINUX, PlatformOS.ANDROID]

    @classmethod
    def resolve(cls) -> PlatformOS:
        """Get the current platform."""
        platform = sys.platform
        result = PlatformOS.UNKNOWN

        if platform in ["win32", "win16", "dos", "cygwin", "msys"]:
            result = PlatformOS.WINDOWS
        if platform.startswith("linux"):
            result = PlatformOS.LINUX
        if platform.startswith("freebsd"):
            result = PlatformOS.FREEBSD
        if platform == "darwin":
            result = PlatformOS.MACOS
        if platform == "ios":
            result = PlatformOS.IOS
        if platform == "android":
            result = PlatformOS.ANDROID
        if platform.startswith("java"):
            result = PlatformOS.UNKNOWN

        return result


OS: Final[PlatformOS] = PlatformOS.resolve()
"""The current platform."""

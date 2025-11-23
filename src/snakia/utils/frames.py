import sys
from types import FrameType


def frame() -> FrameType:
    """Get the current frame."""
    # noqa: W0212 # pylint: disable=W0212
    return sys._getframe(1)

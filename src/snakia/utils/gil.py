from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    GIL_ENABLED: Final[bool] = bool(...)
    """
    Whether the GIL is enabled."""

    def nolock() -> None: ...

else:
    import sys

    if sys.version_info >= (3, 13):
        # noqa: E1101, W0212 # pylint: disable=E1101,W0212
        GIL_ENABLED = sys._is_gil_enabled()
    else:
        GIL_ENABLED = True

    if GIL_ENABLED:
        import time

        def nolock() -> None:
            time.sleep(0.001)

    else:

        def nolock() -> None:
            pass

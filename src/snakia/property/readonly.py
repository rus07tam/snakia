from typing import Any, Callable

from snakia.utils import throw

from .property import Property


class Readonly[T](Property[T]):
    """
    Readonly property.
    """

    def __init__(
        self,
        fget: Callable[[Any], T],
        *,
        strict: bool = False,
    ) -> None:
        super().__init__(
            fget=fget,
            fset=(
                (lambda *_: throw(TypeError("Cannot set readonly property")))
                if strict
                else lambda *_: None
            ),
        )


def readonly[T](value: T, *, strict: bool = False) -> Readonly[T]:
    """Create a readonly property with the given value.

    Args:
        value (T): The value to set the readonly property to.

    Returns:
        Readonly[T]: The readonly property.
    """
    return Readonly(lambda _: value, strict=strict)

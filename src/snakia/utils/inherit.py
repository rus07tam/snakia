from typing import Any, TypeVar

T = TypeVar("T", bound=type)


def inherit(type_: T, attrs: dict[str, Any] | None = None, /, **kwargs: Any) -> T:
    """
    Create a new class that inherits from the given class.

    Args:
        type_: The class to inherit from.
        attrs: A dictionary of attributes to add to the new class.
        **kwargs: Additional attributes to add to the new class.

    Returns:
        A new class that inherits from the given class.
    """
    return type("", (type_,), attrs or {}, **kwargs)  # type: ignore

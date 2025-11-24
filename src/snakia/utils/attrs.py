from typing import Any, TypeVar

T = TypeVar("T")


def get_or_set_attr(obj: Any, name: str, default: T) -> T:
    if not hasattr(obj, name):
        setattr(obj, name, default)
    attr = getattr(obj, name)
    if not isinstance(attr, type(default)):
        setattr(obj, name, default)
        return default
    return attr


def get_attrs(
    obj: Any, *, use_dir: bool = False, of_class: bool = False
) -> dict[str, Any]:
    if of_class and not isinstance(obj, type):
        obj = obj.__class__
    if not use_dir:
        if hasattr(obj, "__dict__"):
            return obj.__dict__  # type: ignore
        if hasattr(obj, "__slots__"):
            return {k: getattr(obj, k) for k in obj.__slots__}
        raise NotImplementedError("Unknown layout")
    else:
        return {k: getattr(obj, k) for k in dir(obj)}

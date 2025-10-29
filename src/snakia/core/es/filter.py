from __future__ import annotations

from typing import Generic, Protocol, TypeVar

from .event import Event

T_contra = TypeVar("T_contra", bound=Event, contravariant=True)


class Filter(Protocol, Generic[T_contra]):
    """Filter for an event."""

    def __call__(self, event: T_contra) -> bool: ...

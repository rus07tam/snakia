from __future__ import annotations

from typing import Generic, NamedTuple, TypeVar

from .event import Event
from .filter import Filter
from .handler import Handler

T_contra = TypeVar("T_contra", bound=Event, contravariant=True)


class Subscriber(NamedTuple, Generic[T_contra]):
    """
    Subscriber for an event."""

    handler: Handler[T_contra]
    filters: Filter[T_contra] | None
    priority: int

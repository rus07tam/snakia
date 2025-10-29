from __future__ import annotations

from typing import Generic, Optional, Protocol, TypeVar

from .action import Action
from .event import Event

T_contra = TypeVar("T_contra", bound=Event, contravariant=True)


class Handler(Protocol, Generic[T_contra]):
    """Handler for an event."""

    def __call__(self, event: T_contra) -> Optional[Action]: ...

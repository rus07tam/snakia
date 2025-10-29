from __future__ import annotations

from pydantic import BaseModel, Field


class Action(BaseModel):
    move: int = Field(default=1)

    @classmethod
    def stop(cls) -> Action:
        """Skip all handlers."""
        return cls(move=2**8)

    @classmethod
    def go_start(cls) -> Action:
        """Go to the first handler."""
        return cls(move=-(2**8))

    @classmethod
    def next(cls, count: int = 1) -> Action:
        """Skip one handler."""
        return cls(move=count)

    @classmethod
    def prev(cls, count: int = 1) -> Action:
        """Go back one handler."""
        return cls(move=-count)

    @classmethod
    def skip(cls, count: int = 1) -> Action:
        """Skip n handlers.

        Args:
            count (int): The number of handlers to skip.
        """
        return cls(move=count + 1)

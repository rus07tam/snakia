from __future__ import annotations

from typing import TYPE_CHECKING, Final, final

from snakia.core.ecs import Processor

if TYPE_CHECKING:
    from .plugin import Plugin


class PluginProcessor(Processor):
    @final
    def __init__(self, plugin: Plugin) -> None:
        self.plugin: Final = plugin

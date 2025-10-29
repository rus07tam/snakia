from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from itertools import count
from typing import Any, TypeVar, cast, overload

import networkx as nx  # type: ignore

from snakia.utils import nolock

from .component import Component
from .processor import Processor

A = TypeVar("A", bound=Component)
B = TypeVar("B", bound=Component)
C = TypeVar("C", bound=Component)
D = TypeVar("D", bound=Component)
E = TypeVar("E", bound=Component)

P = TypeVar("P", bound=Processor)


class System:
    """
    A system is a collection of entities and components that can be processed by processors.
    """

    __processors: list[Processor]
    __components: dict[type[Component], set[int]]
    __entitites: dict[int, dict[type[Component], Component]]
    __entity_counter: count[int]
    __dead_entities: set[int]
    __is_running: bool

    def __init__(self) -> None:
        self.__processors = []
        self.__components = defaultdict(set)
        self.__entitites = defaultdict(dict)
        self.__entity_counter = count(start=1)
        self.__dead_entities = set()
        self.__is_running = False

    @property
    def is_running(self) -> bool:
        """Returns True if the system is running."""
        return self.__is_running

    def full_reset(self) -> None:
        """Resets the system to its initial state."""
        self.__processors = []
        self.__components = defaultdict(set)
        self.__entitites = defaultdict(dict)
        self.__entity_counter = count(start=1)
        self.__dead_entities = set()

    def get_processor(self, processor_type: type[P], /) -> P | None:
        """Returns the first processor of the given type."""
        for processor in self.__processors:
            if isinstance(processor, processor_type):
                return processor
        return None

    def add_processor(self, proccessor: Processor) -> None:
        """Adds a processor to the system."""
        self.__processors.append(proccessor)
        self._sort_processors()

    def remove_processor(self, processor_type: type[Processor]) -> None:
        """Removes a processor from the system."""
        for processor in self.__processors:
            if isinstance(processor, processor_type):
                self.__processors.remove(processor)

    @overload
    def get_components(self, c1: type[A], /) -> Iterable[tuple[int, tuple[A]]]: ...

    @overload
    def get_components(
        self, c1: type[A], c2: type[B], /
    ) -> Iterable[tuple[int, tuple[A, B]]]: ...

    @overload
    def get_components(
        self, c1: type[A], c2: type[B], c3: type[C], /
    ) -> Iterable[tuple[int, tuple[A, B, C]]]: ...

    @overload
    def get_components(
        self, c1: type[A], c2: type[B], c3: type[C], c4: type[D], /
    ) -> Iterable[tuple[int, tuple[A, B, C, D]]]: ...

    @overload
    def get_components(
        self,
        c1: type[A],
        c2: type[B],
        c3: type[C],
        c4: type[D],
        c5: type[E],
        /,
    ) -> Iterable[tuple[int, tuple[A, B, C, D]]]: ...

    def get_components(
        self, *component_types: type[Component]
    ) -> Iterable[tuple[int, tuple[Component, ...]]]:
        """Returns all entities with the given components."""
        entity_set = set.intersection(
            *(self.__components[component_type] for component_type in component_types)
        )
        for entity in entity_set:
            yield (
                entity,
                tuple(
                    self.__entitites[entity][component_type]
                    for component_type in component_types
                ),
            )

    @overload
    def get_components_of_entity(
        self, entity: int, c1: type[A], /
    ) -> tuple[A | None]: ...

    @overload
    def get_components_of_entity(
        self, entity: int, c1: type[A], c2: type[B], /
    ) -> tuple[A | None, B | None]: ...

    @overload
    def get_components_of_entity(
        self, entity: int, c1: type[A], c2: type[B], c3: type[C], /
    ) -> tuple[A | None, B | None, C | None]: ...

    @overload
    def get_components_of_entity(
        self,
        entity: int,
        c1: type[A],
        c2: type[B],
        c3: type[C],
        c4: type[D],
        /,
    ) -> tuple[A | None, B | None, C | None, D | None]: ...

    @overload
    def get_components_of_entity(
        self,
        entity: int,
        c1: type[A],
        c2: type[B],
        c3: type[C],
        c4: type[D],
        c5: type[E],
        /,
    ) -> tuple[A | None, B | None, C | None, D | None, E | None]: ...

    def get_components_of_entity(
        self, entity: int, /, *component_types: type[Component]
    ) -> tuple[Any, ...]:
        """Returns the components of the given entity."""
        entity_dict = self.__entitites[entity]
        return (
            *(
                entity_dict.get(component_type, None)
                for component_type in component_types
            ),
        )

    def get_component(self, component_type: type[C], /) -> Iterable[tuple[int, C]]:
        """Returns all entities with the given component."""
        for entity in self.__components[component_type].copy():
            yield entity, cast(C, self.__entitites[entity][component_type])

    @overload
    def get_component_of_entity(
        self, entity: int, component_type: type[C], /
    ) -> C | None: ...

    @overload
    def get_component_of_entity(
        self, entity: int, component_type: type[C], /, default: D
    ) -> C | D: ...

    def get_component_of_entity(
        self,
        entity: int,
        component_type: type[Component],
        /,
        default: Any = None,
    ) -> Any:
        """Returns the component of the given entity."""
        return self.__entitites[entity].get(component_type, default)

    def add_component(self, entity: int, component: Component) -> None:
        """Adds a component to an entity."""
        component_type = type(component)
        self.__components[component_type].add(entity)
        self.__entitites[entity][component_type] = component

    def has_component(self, entity: int, component_type: type[Component]) -> bool:
        """Returns True if the entity has the given component."""
        return component_type in self.__entitites[entity]

    def has_components(self, entity: int, *component_types: type[Component]) -> bool:
        """Returns True if the entity has all the given components."""
        components_dict = self.__entitites[entity]
        return all(comp_type in components_dict for comp_type in component_types)

    def remove_component(self, entity: int, component_type: type[C]) -> C | None:
        """Removes a component from an entity."""
        self.__components[component_type].discard(entity)
        if not self.__components[component_type]:
            del self.__components[component_type]
        return self.__entitites[entity].pop(component_type)  # type: ignore

    def create_entity(self, *components: Component) -> int:
        """Creates an entity with the given components."""
        entity = next(self.__entity_counter)
        if entity not in self.__entitites:
            self.__entitites[entity] = {}
        for component in components:
            component_type = type(component)
            self.__components[component_type].add(entity)
            if component_type not in self.__entitites[entity]:
                self.__entitites[entity][component_type] = component
        return entity

    def delete_entity(self, entity: int, immediate: bool = False) -> None:
        """Deletes an entity."""
        if immediate:
            for component_type in self.__entitites[entity]:
                self.__components[component_type].discard(entity)
                if not self.__components[component_type]:
                    del self.__components[component_type]
            del self.__entitites[entity]
        else:
            self.__dead_entities.add(entity)

    def entity_exists(self, entity: int) -> bool:
        """Returns True if the entity exists."""
        return entity in self.__entitites and entity not in self.__dead_entities

    def start(self) -> None:
        """Starts the system."""
        self.__is_running = True
        while self.__is_running:
            self.update()
            nolock()

    def stop(self) -> None:
        """Stops the system."""
        self.__is_running = False

    def update(self) -> None:
        """Updates the system."""
        self._clear_dead_entities()
        for processor in self.__processors:
            processor.process(self)

    def _clear_dead_entities(self) -> None:
        for entity in self.__dead_entities:
            self.delete_entity(entity, immediate=True)
        self.__dead_entities = set()

    def _sort_processors(self) -> None:
        processors = self.__processors
        graph: nx.DiGraph[Processor] = nx.DiGraph()
        for p in processors:
            graph.add_node(p)
        for p in processors:
            for after_cls in p.after:
                for q in processors:
                    if isinstance(q, after_cls):
                        graph.add_edge(q, p)
            for before_cls in p.before:
                for q in processors:
                    if isinstance(q, before_cls):
                        graph.add_edge(p, q)
        sorted_processors = list(nx.topological_sort(graph))
        self.__processors = sorted_processors

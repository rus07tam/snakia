import operator
from typing import Any, Callable, overload

from snakia.utils import to_async

from .async_bindable import AsyncBindable
from .base_bindable import ValueChanged
from .bindable import Bindable
from .concat import concat


@overload
def combine[A, R](
    source1: Bindable[A] | AsyncBindable[A],
    /,
    *,
    combiner: Callable[[A], R],
) -> Bindable[R]: ...


@overload
def combine[A, B, R](
    source1: Bindable[A] | AsyncBindable[A],
    source2: Bindable[B] | AsyncBindable[B],
    /,
    *,
    combiner: Callable[[A, B], R],
) -> Bindable[R]: ...


@overload
def combine[A, B, C, R](
    source1: Bindable[A] | AsyncBindable[A],
    source2: Bindable[B] | AsyncBindable[B],
    source3: Bindable[C] | AsyncBindable[C],
    /,
    *,
    combiner: Callable[[A, B, C], R],
) -> Bindable[R]: ...


@overload
def combine[A, B, C, D, R](
    source1: Bindable[A] | AsyncBindable[A],
    source2: Bindable[B] | AsyncBindable[B],
    source3: Bindable[C] | AsyncBindable[C],
    source4: Bindable[D] | AsyncBindable[D],
    /,
    *,
    combiner: Callable[[A, B, C, D], R],
) -> Bindable[R]: ...


@overload
def combine[A, B, C, D, R](
    source1: Bindable[A] | AsyncBindable[A],
    source2: Bindable[B] | AsyncBindable[B],
    source3: Bindable[C] | AsyncBindable[C],
    source4: Bindable[D] | AsyncBindable[D],
    /,
    *,
    combiner: Callable[[A, B, C, D], R],
) -> Bindable[R]: ...


@overload
def combine[R](
    *sources: Bindable[Any] | AsyncBindable[Any],
    combiner: Callable[..., R],
) -> Bindable[R]: ...


def combine[R](
    *sources: Bindable[Any] | AsyncBindable[Any],
    combiner: Callable[..., R],
) -> Bindable[R]:
    combined = Bindable[R]()
    values = [*map(lambda s: s.value, sources)]

    for i, source in enumerate(sources):

        def make_subscriber(
            index: int,
        ) -> Callable[[ValueChanged[Any]], None]:
            return concat(
                lambda v: operator.setitem(values, index, v.new_value),
                lambda _: combiner(*values),
            )

        if isinstance(source, Bindable):
            source.subscribe(make_subscriber(i))
        else:
            source.subscribe(to_async(make_subscriber(i)))
    return combined

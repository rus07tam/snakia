import sys
from types import TracebackType
from typing import Any, Callable, Protocol, final


class ExceptionHook[T: BaseException](Protocol):
    def __call__(
        self, exception: T, frame: TracebackType | None, /
    ) -> bool | None: ...


@final
class _ExceptionManager:
    def __init__(self) -> None:
        self.__hooks: list[tuple[type[BaseException], ExceptionHook[Any]]] = []
        sys.excepthook = self._excepthook

    def hook_exception[T: BaseException](
        self, exception_type: type[T], func: ExceptionHook[T]
    ) -> ExceptionHook[T]:
        self.__hooks.append((exception_type, func))
        return func

    def on_exception[T: BaseException](
        self, exception_type: type[T]
    ) -> Callable[[ExceptionHook[T]], ExceptionHook[T]]:
        def inner(func: ExceptionHook[T]) -> ExceptionHook[T]:
            self.hook_exception(exception_type, func)
            return func

        return inner

    def _on_except(
        self,
        type_: type[BaseException],
        exception: BaseException,
        frame: TracebackType | None,
    ) -> None:
        for hook_type, hook_func in self.__hooks:
            if hook_type == type_ or issubclass(hook_type, type_):
                result = hook_func(exception, frame)
                if result:
                    break

    def _excepthook(
        self,
        type_: type[BaseException],
        exception: BaseException,
        frame: TracebackType | None,
    ) -> None:
        while True:
            try:
                self._on_except(type_, exception, frame)
                break
            except BaseException as e:  # noqa: W0718  # pylint: disable=W0718
                if e is exception:
                    return
                type_, exception = type(e), e


ExceptionManager = _ExceptionManager()

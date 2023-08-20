import math
import time
from contextlib import ContextDecorator, AsyncContextDecorator
from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, Dict, Optional, Union


class TimerError(Exception):
    """Кастомная ошибка для класса Timer"""


@dataclass
class Timer(AsyncContextDecorator, ContextDecorator):
    """Таймер для замера времени выполнения функций реализованный как класс, контекстный менеджер и декоратор"""

    timers: ClassVar[Dict[str, float]] = {}

    _start_time: Optional[float] = field(default=None, init=False, repr=False)
    name: Optional[str] = None
    text: Union[str, Callable[[float], str]] = "Время выполнения: {:0.4f} сек."
    logger: Optional[Callable[[str], None]] = print
    elapsed_time: float = field(default=math.nan, init=False, repr=False)

    def __post_init__(self) -> None:
        """Добавление таймера в словарь для сохранения именованных таймеров"""
        if self.name:
            self.timers.setdefault(self.name, 0)

    def start(self) -> None:
        """Запуск нового таймер"""
        if self._start_time is not None:
            raise TimerError(
                "Таймер уже запущен. Вызовите метод .stop() для остановки запущенного таймера"
            )

        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Остановка таймера и вывод времени выполнения"""
        if self._start_time is None:
            raise TimerError(
                "Таймер не запущен. Вызовите метод .start() для запуска нового таймера"
            )

        self.elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        if self.logger:
            if callable(self.text):
                text = self.text(self.elapsed_time)
            else:
                attributes = {
                    "имя": self.name,
                    "milliseconds": self.elapsed_time * 1000,
                    "seconds": self.elapsed_time,
                    "minutes": self.elapsed_time / 60,
                }
                text = self.text.format(self.elapsed_time, **attributes)
            self.logger(text)
        if self.name:
            self.timers[self.name] += self.elapsed_time

        return self.elapsed_time

    def __enter__(self) -> "Timer":
        """Запуск нового таймера в виде синхронного контекстного менеджера"""
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Остановка таймера вызванного в виде синхронного контекстного менеджера"""
        self.stop()

    async def __aenter__(self) -> "Timer":
        """Запуск нового таймера в виде асинхронного контекстного менеджера"""
        self.start()
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        """Остановка таймера вызванного в виде асинхронного контекстного менеджера"""
        self.stop()

from typing import Callable, Coroutine, Any

from src.domain.events.base import DomainEvent


EventHandler = Callable[[DomainEvent], Coroutine[Any, Any, None]]
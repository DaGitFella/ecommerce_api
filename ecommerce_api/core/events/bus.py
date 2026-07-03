from collections import defaultdict
from typing import TypeVar, Callable, Awaitable
from .base import DomainEvent

E = TypeVar('E', bound=DomainEvent)
Handler = Callable[[E], Awaitable[None]]

class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[Handler]] = defaultdict(list)
    
    def subscribe(self, event_type: type[E], handler: Handler) -> None:
        self._handlers[event_type].append(handler)
    
    async def publish(self, event: DomainEvent) -> None:
        for handler in self._handlers[type(event)]:
            await handler(event)
            
from ecommerce_api.core.events.base import DomainEvent
from ecommerce_api.core.events.bus import EventBus


class FakeEventBus(EventBus):
    def __init__(self):
        super().__init__()
        self.published: list[DomainEvent] = []

    async def publish(self, event):
        self.published.append(event)

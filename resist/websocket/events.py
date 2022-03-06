from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Callable, Generic, Literal, TypeVar

import attr

if TYPE_CHECKING:
    from ..client import WebSocketClient

    Callback = Callable[..., Any]

__all__ = ("EVENT_MAPPING", "Events", "Event", "Listener", "Collector")
_log = logging.getLogger(__name__)

Check = Callable[..., bool]
NameT = TypeVar(
    "NameT",
    bound=Literal[
        "Error",
        "Authenticated",
        "Pong",
        "Ready",
        "Message",
        "MessageUpdate",
        "MessageDelete",
        "ChannelCreate",
        "ChannelUpdate",
        "ChannelDelete",
        "ChannelGroupJoin",
        "ChannelGroupLeave",
        "ChannelStartTyping",
        "ChannelStopTyping",
        "ChannelAck",
        "ServerUpdate",
        "ServerDelete",
        "ServerMemberUpdate",
        "ServerMemberJoin",
        "ServerMemberLeave",
        "ServerRoleUpdate",
        "ServerRoleDelete",
        "UserUpdate",
        "UserRelationship",
    ],
)


EVENT_MAPPING: dict[str, Event[Any]] = {}


@attr.s(slots=True, kw_only=True)
class Listener:
    """A class which represents an event listener.

    Parameters
    ----------
    once: :class:`bool`
        If the listener should be called one a lifetime.

    callback: Callable[..., :class:`bool`]
        The callback of the listener.

    check: Callable[..., :class:`bool`]
        The check to run before dispatching.
    """

    once: bool = attr.field(repr=True)
    callback: Callback = attr.field(repr=False)
    check: Check = attr.field(repr=False)

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return await self.callback(*args, **kwargs)


@attr.s(slots=True, kw_only=True)
class Collector:
    """A class which represents an event collector.

    Parameters
    ----------
    once: :class:`bool`
        If the listener should be called one a lifetime.

    callback: Callable[..., :class:`bool`]
        The callback of the collector.

    check: Callable[..., :class:`bool`]
        The check to run before dispatching.
    """

    once: bool = attr.field(repr=True)
    callback: Callback = attr.field(repr=False)
    check: Check = attr.field(repr=False)

    amount: int = attr.field(repr=True)
    timeout: timedelta = attr.field(repr=True)

    queue: asyncio.Queue[Any] = attr.field(init=False, repr=False)
    first: datetime = attr.field(init=False, repr=True)
    recent: datetime = attr.field(init=False, repr=True)

    def __attrs_post_init__(self) -> None:
        self.queue = asyncio.Queue[Any](maxsize=self.amount)

    async def __call__(self, *args: Any, **_: Any) -> Any:
        if not hasattr(self, "first"):
            self.first = datetime.utcnow()

        self.recent = datetime.utcnow()
        if not (self.recent - self.first) <= self.timeout:

            while not self.queue.empty():
                self.queue.get_nowait()

            return

        await self.queue.put(args)
        self.queue.task_done()

        if self.queue.full():
            items = [self.queue.get_nowait() for _ in range(self.amount)]
            await self.callback(*list(zip(*items)))


@attr.s(slots=True)
class Event(Generic[NameT]):
    """A class which represents events.

    This class is responsbile for handling dispatch
    and subscription of events.

    Attributes
    ----------
    name: :class:`str`
        The name of the event.

    listeners: :class:`list`
        A list of :class:`.Listener` subscribed to the event.

    collectors: :class:`list`
        A list of :class:`.Collector` subscribed to the event.
    """

    name: NameT = attr.field(repr=True)

    listeners: list[Listener] = attr.field(init=False, repr=False)
    collectors: list[Collector] = attr.field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.listeners = []
        self.collectors = []

        EVENT_MAPPING[self.name] = self

    def subscribe(self, listener: Listener | Collector) -> None:
        """Subscribes a :class:`.Listener` or a :class:`.Collector`
        To the event this method is being called from.

        Parameters
        ----------
        listener: :class:`.Listener` | :class:`.Collector`
            The listener or collector to subscribe to this event.

        Raises
        ------
        :exc:`TypeError`
            Raised when receiving a listener that is not a type of
            :class:`.Listener` or :class:`.Collector`.
        """
        if isinstance(listener, Listener):
            if not asyncio.iscoroutinefunction(listener.callback):
                raise TypeError("Callback has to be a coroutine function.") from None

            return self.listeners.append(listener)

        elif isinstance(listener, Collector):
            if not asyncio.iscoroutinefunction(listener.callback):
                raise TypeError("Callback has to be a coroutine function.") from None

            return self.collectors.append(listener)

        raise TypeError(f"Unknown listener type {type(listener)}") from None

    def dispatch(self, client: WebSocketClient, *args: Any) -> list[asyncio.Task[Any]]:
        """Dispatches the event.

        Parameters
        ----------
        client: :class:`.WebSocketClient`
            The client to dispatch from.

        args: Any
            The payload to dispatch the event with.

        Returns
        -------
        :class:`list`
            A list of :class:`asyncio.Task` created from dispatching.
        """
        tasks: list[asyncio.Task[Any]] = []

        listeners = self.listeners[:]
        collectors = self.collectors[:]

        for index, listener in enumerate(listeners):
            if not listener.check(*args):
                continue

            if listener.once is True:
                self.listeners.pop(index)

            tasks.append(client.loop.create_task(listener(*args)))

        for index, collector in enumerate(collectors):
            if not collector.check(*args):
                continue

            if collector.once is True:
                self.collectors.pop(index)

            tasks.append(client.loop.create_task(collector(*args)))

        _log.debug(f"DISPATCHED {self.name}")
        return tasks


@type.__call__
class Events:
    """Container class for all events.

    Format is in `SCREAMING_SNAKE_CASE`,
    E.g `ServerMemberUpdate` => `SERVER_MEMBER_UPDATE`

    For all events see https://developers.revolt.chat/websockets/events
    """

    ERROR = Event("Error")
    AUTHENTICATED = Event("Authenticated")
    PONG = Event("Pong")
    READY = Event("Ready")

    MESSAGE = Event("Message")
    MESSAGE_UPDATE = Event("MessageUpdate")
    MESSAGE_DELETE = Event("MessageDelete")

    CHANNEL_CREATE = Event("ChannelCreate")
    CHANNEL_UPDATE = Event("ChannelUpdate")
    CHANNEL_DELETE = Event("ChannelDelete")

    CHANNEL_GROUP_JOIN = Event("ChannelGroupJoin")
    CHANNEL_GROUP_LEAVE = Event("ChannelGroupLeave")

    CHANNEL_START_TYPING = Event("ChannelStartTyping")
    CHANNEL_STOP_TYPING = Event("ChannelStopTyping")
    CHANNEL_ACK = Event("ChannelAck")

    SERVER_UPDATE = Event("ServerUpdate")
    SERVER_DELETE = Event("ServerDelete")

    SERVER_MEMBER_UPDATE = Event("ServerMemberUpdate")
    SERVER_MEMBER_JOIN = Event("ServerMemberJoin")
    SERVER_MEMBER_LEAVE = Event("ServerMemberLeave")

    SERVER_ROLE_UPDATE = Event("ServerRoleUpdate")
    SERVER_ROLE_DELETE = Event("ServerRoleDelete")

    USER_UPDATE = Event("UserUpdate")
    USER_RELATIONSHIP = Event("UserRelationship")

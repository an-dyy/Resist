from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Callable

from attrs import define, field

from .rest import RESTClient
from .websocket import Collector, Event, Listener, WebSocketHandler

if TYPE_CHECKING:
    Callback = Callable[..., Any]
    Check = Callable[..., bool]


@define
class WebSocketClient:
    """The class used to interact with the API.
    This is the main interface of the API wrapper.


    Parameters
    ----------
    token: :class:`str`
        The token used for authorisation.

    loop: :class:`asyncio.AbstractEventLoop`
        The loop to use for async IO.

    Attributes
    ----------
    token: :class:`str`
        The token used for authorisation.

    loop: :class:`asyncio.AbstractEventLoop`
        The loop to use for async IO.

    sock: :class:`.WebSocketHandler`
        The websocket handler for the client.

    rest: :class:`.RESTClient`
        The rest client being used.
    """

    token: str = field(repr=False)
    loop: asyncio.AbstractEventLoop = field(kw_only=True, repr=False, default=None)

    sock: WebSocketHandler = field(init=False, repr=False)
    rest: RESTClient = field(init=False, repr=False)

    def on(
        self, event: Event[Any], check: Check = lambda *_: True
    ) -> Callable[..., Listener]:
        """Registers a callback to an event.

        Parameters
        ----------
        event: :class:`.Event`
            The event to subscribe the callback to.

        check: Callable[..., :class:`bool`]
            The check the event must pass first in order to be dispatched.

        Raises
        ------
        :exc:`TypeError`
            The function being wrapped is not a coroutine function.

        Returns
        -------
        :class:`.Listener`
            The registered listener.
        """

        def inner(func: Callback) -> Listener:
            listener = Listener(once=False, callback=func, check=check)
            event.subscribe(listener)

            return listener

        return inner

    def once(
        self, event: Event[Any], check: Check = lambda *_: True
    ) -> Callable[..., Listener]:
        """Registers a one-time callback to an event.

        Parameters
        ----------
        event: :class:`.Event`
            The event to subscribe the callback to.

        check: Callable[..., :class:`bool`]
            The check the event must pass first in order to be dispatched.

        Raises
        ------
        :exc:`TypeError`
            The function being wrapped is not a coroutine function.

        Returns
        -------
        :class:`.Listener`
            The registered listener.
        """

        def inner(func: Callback) -> Listener:
            listener = Listener(once=True, callback=func, check=check)
            event.subscribe(listener)

            return listener

        return inner

    def collect(
        self,
        event: Event[Any],
        amount: int,
        timeout: None | timedelta,
        once: bool = False,
        check: Check = lambda *_: True,
    ) -> Callable[..., Collector]:
        """Registers a collector to an event.

        Parameters
        ----------
        event: :class:`.Event`
            The event to subscribe the callback to.

        check: Callable[..., :class:`bool`]
            The check the event must pass first in order to be dispatched.

        Raises
        ------
        :exc:`TypeError`
            The function being wrapped is not a coroutine function.

        Returns
        -------
        :class:`.Collector`
            The registered collector.
        """
        timeout = timeout or timedelta.max

        def inner(func: Callback) -> Collector:
            collector = Collector(
                once=once, callback=func, check=check, amount=amount, timeout=timeout
            )

            event.subscribe(collector)
            return collector

        return inner

    def dispatch(self, event: Event[Any], *args: Any) -> list[asyncio.Task[Any]]:
        """Dispatches an event.

        Parameters
        ----------
        event: :class:`.Event`
            The event to dispatch.

        args: Any
            The payload to dispatch the event with.

        Returns
        -------
        :class:`list`
            A list of :class:`asyncio.Task` created from the dispatch.
        """
        return event.dispatch(self, *args)

    async def connect(self) -> None:
        """Starts the connection to the API."""

        if self.loop is None:
            self.loop = asyncio.get_running_loop()

        self.rest = await RESTClient.connect(self)
        self.sock = WebSocketHandler(self)

        await self.sock.connect()

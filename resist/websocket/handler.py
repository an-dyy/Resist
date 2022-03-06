from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Callable, NamedTuple, cast

import aiohttp
import attr

from ..types import Auth
from .events import EVENT_MAPPING

if TYPE_CHECKING:
    from ..client import WebSocketClient
    from ..rest import RESTClient


__all__ = ("WebSocketHandler",)
_log = logging.getLogger(__name__)


class WSMessage(NamedTuple):
    type: aiohttp.WSMsgType
    json: Callable[..., dict[Any, Any]]


@attr.s(slots=True)
class WebSocketHandler:
    """The class used to handle the websocket.
    This class handles things such as events.

    Parameters
    ----------
    client: :class:`.WebSocketClient`
        The client being used for the connection.
    """

    client: WebSocketClient = attr.field(repr=False)
    rest: RESTClient = attr.field(init=False, repr=False)
    sock: aiohttp.ClientWebSocketResponse = attr.field(init=False, repr=False)

    events: dict[str, str] = attr.field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.rest = self.client.rest

    async def connect(self) -> None:
        payload = Auth(type="Authenticate", token=self.client.token)
        context, session = (self.rest.context, self.rest.session)
        self.sock = await session.ws_connect(context["ws"], heartbeat=10)

        await self.sock.send_json(payload)
        await self.read()

    async def read(self) -> None:
        async for message in self.sock:
            message = cast(WSMessage, message)

            if message.type is not aiohttp.WSMsgType.TEXT:
                continue

            data = message.json()
            _log.debug(f"RECEIVED {data['type']}")

            if event := EVENT_MAPPING.get(data["type"]):
                event.dispatch(self.client, data)
                continue

            _log.debug(f"UNKNOWN EVENT {data['type']}")

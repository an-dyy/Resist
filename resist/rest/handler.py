from __future__ import annotations

from typing import TYPE_CHECKING, Any

import aiohttp
import attr
from typing_extensions import Self

from ..types import APIContext

if TYPE_CHECKING:
    from ..client import WebSocketClient


@attr.s(slots=True)
class RESTClient:
    """A class which handles the REST API.

    Parameters
    ----------
    client: :class:`.WebSocketClient`
        The client currently being used.

    token: :class:`str`
        The token to use for authorisation.

    url: :class:`str`
        The URL to use for the API.

    Attributes
    ----------
    client: :class:`.WebSocketClient`
        The client currently being used.

    token: :class:`str`
        The token to use for authorisation.

    url: :class:`str`
        The URL to use for the API.

    session: :class:`aiohttp.ClientSession`
        The ClientSession used for requests.

    context: :class:`.APIContext`
        The context of the API.
    """

    client: WebSocketClient = attr.field(repr=False)
    token: str = attr.field(repr=False)
    url: str = attr.field(repr=True)

    session: aiohttp.ClientSession = attr.field(init=False, repr=False)
    context: APIContext = attr.field(init=False, repr=True)

    @classmethod
    async def connect(
        cls: type[Self], client: WebSocketClient, url: str = "https://api.revolt.chat/"
    ) -> Self:
        """Creates a RESTClient and connects.

        Parameters
        ----------
        client: :class:`.WebSocketClient`
            The client to use for the API.

        url: :class:`str`
            The URL to use for the API.

        Returns
        -------
        :class:`.RESTClient`
            A created RESTClient from the parameters given.
        """
        headers = {"x-bot-token": client.token, "User-Agent": "Resist v0.1.0-alpha"}

        self: Self = cls(client, client.token, url)
        self.session = aiohttp.ClientSession(headers=headers)

        async with self.session.get(url) as resp:
            self.context = APIContext(**(await resp.json()))

        return self

    async def request(self, method: str, path: str, **kwargs: Any) -> Any:
        """Makes a request to the API.

        Parameters
        ----------
        method: :class:`str`
            The method of the request.

        path: :class:`str`
            The path of the request.

        kwargs: Any
            kwargs to pass to `aiohttp.ClientSession.request`

        Returns
        -------
        Any
            The response of the request.
        """
        path = self.url + path

        async with self.session.request(method, path, **kwargs) as resp:
            return await resp.json()

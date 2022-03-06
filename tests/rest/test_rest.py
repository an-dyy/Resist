from __future__ import annotations

from unittest import mock

import aiohttp
import pytest

import resist


class TestRESTClient:
    @pytest.fixture()
    def client(self) -> resist.WebSocketClient:
        return resist.WebSocketClient("REVOLT_TOKEN")

    @pytest.fixture()
    def rest(self, client: resist.WebSocketClient) -> resist.RESTClient:
        return resist.RESTClient(client, client.token, url="foo")

    def test_attributes(self, rest: resist.RESTClient) -> None:
        assert isinstance(rest.client, resist.WebSocketClient)
        assert isinstance(rest.token, str) and rest.token == "REVOLT_TOKEN"
        assert isinstance(rest.url, str) and rest.url == "foo"

        assert not hasattr(rest, "session")
        assert not hasattr(rest, "context")

    @pytest.mark.asyncio
    async def test_connect(self, client: resist.WebSocketClient) -> None:
        with mock.patch.object(resist.RESTClient, "connect") as _:
            ...

        with mock.patch.object(aiohttp.ClientSession, "get") as get:
            get.json = mock.MagicMock(return_value={"baz": "qux"})

            with pytest.raises(TypeError):
                rest = await resist.RESTClient.connect(client, "bar")

                assert isinstance(rest, resist.RESTClient)
                self.test_attributes(rest)

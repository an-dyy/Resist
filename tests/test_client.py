from __future__ import annotations

import asyncio
import types
from typing import cast
from unittest import mock

import pytest

import resist


class TestWebSocketClient:
    @pytest.fixture()
    def client(self) -> resist.WebSocketClient:
        return resist.WebSocketClient("REVOLT_TOKEN")

    def test_attributes(self, client: resist.WebSocketClient) -> None:
        assert isinstance(client, resist.WebSocketClient)
        assert client.token is not None and isinstance(client.token, str)

        assert not hasattr(client, "sock")
        assert not hasattr(client, "rest")
        assert hasattr(client, "loop") and client.loop is None

    @pytest.mark.asyncio
    async def test_connect(self, client: resist.WebSocketClient) -> None:
        assert client.loop is None

        with mock.patch.object(resist.WebSocketHandler, "connect") as connect:
            connect = cast(mock.AsyncMock, connect)

            with mock.patch.object(resist.RESTClient, "connect") as rest:
                rest = cast(mock.AsyncMock, rest)
                await client.connect()

            rest.assert_awaited_once()
            connect.assert_awaited_once()

        assert client.loop is not None

    def test_on(self, client: resist.WebSocketClient) -> None:
        @client.on(resist.Events.MESSAGE)
        async def test_register() -> None:
            ...

        assert not isinstance(test_register, types.FunctionType)
        assert isinstance(test_register, resist.Listener)

        with pytest.raises(TypeError):

            @client.on(resist.Events.MESSAGE)
            def _() -> None:
                ...

        assert test_register.once is not True
        assert len(resist.Events.MESSAGE.listeners) == 1

        resist.Events.MESSAGE.listeners.pop()

    @pytest.mark.asyncio
    async def test_once(self, client: resist.WebSocketClient) -> None:
        @client.once(resist.Events.MESSAGE)
        async def test_once_register() -> None:
            ...

        assert isinstance(test_once_register, resist.Listener)
        assert len(resist.Events.MESSAGE.listeners) == 1
        assert test_once_register.once is True

        resist.Events.MESSAGE.listeners.pop()

    def test_collect(self, client: resist.WebSocketClient) -> None:
        @client.collect(resist.Events.MESSAGE, amount=5, timeout=None)
        async def test_collect_register() -> None:
            ...

        assert isinstance(test_collect_register, resist.Collector)
        assert len(resist.Events.MESSAGE.collectors) == 1
        assert test_collect_register.once is False

        @client.collect(resist.Events.MESSAGE, amount=5, timeout=None, once=True)
        async def test_collect_once_register() -> None:
            ...

        assert isinstance(test_collect_once_register, resist.Collector)
        assert len(resist.Events.MESSAGE.collectors) == 2
        assert test_collect_once_register.once is True

        resist.Events.MESSAGE.collectors.pop()
        resist.Events.MESSAGE.collectors.pop()

    @pytest.mark.asyncio
    async def test_dispatch(self, client: resist.WebSocketClient) -> None:
        client.loop = asyncio.get_running_loop()

        with pytest.raises(Exception):

            @client.on(resist.Events.MESSAGE)
            async def test_dispatch() -> None:
                raise Exception

            assert isinstance(test_dispatch, resist.Listener)

            tasks = client.dispatch(resist.Events.MESSAGE)
            await asyncio.gather(*tasks)

        resist.Events.MESSAGE.listeners.pop()

from __future__ import annotations

from typing import cast
from unittest import mock

import pytest

import resist


class TestWebSocketHandler:
    @pytest.fixture()
    def client(self) -> resist.WebSocketClient:
        return resist.WebSocketClient("REVOLT_TOKEN")

    @pytest.fixture()
    def sock(self, client: resist.WebSocketClient) -> resist.WebSocketHandler:
        client.rest = resist.RESTClient(client, client.token, "URL")
        client.rest.session = mock.MagicMock()
        client.rest.session.ws_connect = mock.AsyncMock()
        client.rest.context = resist.APIContext(
            revolt="foo",
            features="bar",  # type: ignore
            ws="baz",
            app="qux",
            vapid="quux",
        )

        sock = resist.WebSocketHandler(client)
        sock.sock = mock.MagicMock()
        return sock

    def test_attributes(self, sock: resist.WebSocketHandler) -> None:
        assert sock.client is not None and isinstance(sock.client, resist.WebSocketClient)
        assert sock.rest is not None and isinstance(sock.rest, resist.RESTClient)

    @pytest.mark.asyncio
    async def test_connect(self, sock: resist.WebSocketHandler) -> None:
        ws_connect = cast(mock.AsyncMock, sock.rest.session.ws_connect)

        with mock.patch.object(resist.WebSocketHandler, "read") as read:
            sock.sock = mock.MagicMock()
            sock.sock.send_json = mock.AsyncMock()

            read = cast(mock.AsyncMock, read)
            await sock.connect()

        ws_connect.assert_awaited_once()
        sock.sock.send_json.assert_awaited_once()  # type: ignore
        read.assert_awaited_once()

    def test_read(self, sock: resist.WebSocketHandler):
        assert hasattr(sock.sock, "receive")
        assert hasattr(sock.sock, "__anext__")
        assert hasattr(sock.sock, "__aiter__")

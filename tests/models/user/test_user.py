from __future__ import annotations

import pytest

import resist


class TestUser:
    @pytest.fixture()
    def client(self) -> resist.WebSocketClient:
        return resist.WebSocketClient("REVOLT_TOKEN")

    def test_attributes(self, client: resist.WebSocketClient) -> None:
        user = resist.User(client, {"_id": "foo", "username": "bar"})

        assert user.unique == "foo"
        assert user.username == "bar"
        assert hasattr(user, "fetch")
        assert hasattr(user, "cache")

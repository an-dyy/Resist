from __future__ import annotations

from datetime import datetime, timezone

import pytest

import resist


class TestMessage:
    @pytest.fixture()
    def client(self) -> resist.WebSocketClient:
        return resist.WebSocketClient("REVOLT_TOKEN")

    def test_user_message(self, client: resist.WebSocketClient) -> None:
        message = resist.Message(
            client,
            {
                "_id": "foobar",
                "nonce": "resist",
                "channel": "98765",
                "author": "012345",
                "content": r"100% coverage is a dream",
                "edited": {"$date": "2022-03-10T13:21:01.356Z"},
            },
        )

        edited_at = datetime(2022, 3, 10, 13, 21, 1, 356000, tzinfo=timezone.utc)

        assert message.unique == "foobar"
        assert message.nonce == "resist"
        assert message.channel == "98765"
        assert message.author == "012345"
        assert message.content == r"100% coverage is a dream"
        assert message.edited_at == edited_at
        assert len(message.attachments) == 0
        assert len(message.embeds) == 0
        assert len(message.mentions) == 0
        assert len(message.replies) == 0
        assert message.masquerade is None
        assert hasattr(message, "fetch")
        assert hasattr(message, "cache")

    def test_system_message(self, client: resist.WebSocketClient) -> None:
        m1 = resist.Message(
            client,
            {
                "_id": "system-message1",
                "channel": "98765",
                "author": "system",  # who is the author for system messages?
                "content": {"type": "text", "content": "This is a test"},
            },
        )
        m2 = resist.Message(
            client,
            {
                "_id": "system-message2",
                "channel": "98765",
                "author": "system",
                "content": {"type": "user_added", "id": "12345"},
            },
        )
        m3 = resist.Message(
            client,
            {
                "_id": "system-message3",
                "channel": "98765",
                "author": "system",
                "content": {"type": "channel_renamed", "by": "12345"},
            },
        )

        assert m1.content == "This is a test"
        assert m1.system == {"type": "text", "content": "This is a test"}

        assert m2.content == "type:user_added id:12345"

        assert m3.content == "type:channel_renamed by:12345"

    def test_replies(self, client: resist.WebSocketClient) -> None:
        message = resist.Message(
            client,
            {
                "_id": "replying",
                "channel": "98765",
                "author": "12345",
                "content": "this is a reply",
                "replies": [
                    "foobar",
                    "system-message1",
                    "system-message2",
                    "system-message3",
                ],
            },
        )

        assert message.replies == [
            m for m in resist.Message.cache.root.values() if m.unique != "replying"
        ]

from __future__ import annotations

import pytest

import resist


class TestPresence:
    @pytest.fixture()
    def presence(self) -> resist.Presence:
        return resist.Presence({"text": "foo", "presence": "Online"})

    def test_attributes(self, presence: resist.Presence) -> None:
        assert presence.text == "foo"
        assert presence.kind == "Online"

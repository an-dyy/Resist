from __future__ import annotations

import pytest

import resist


class TestEmbed:
    def test_user_embed(self) -> None:
        attachment = resist.Asset(
            {
                "_id": "1",
                "tag": "attachments",
                "size": 1,
                "filename": "a.png",
                "metadata": {},
                "content_type": "image/png",
            }
        )
        embed = resist.Embed(title="resist", url="github.com/resist", media=attachment)

        assert embed.title == "resist"
        assert embed.url == "github.com/resist"
        assert embed.data == {
            "title": "resist",
            "type": "Text",
            "url": "github.com/resist",
            "media": attachment.data,
        }

    def test_api_embed(self) -> None:
        data = {"type": "Text", "icon_url": "abc", "title": "resist"}

        e1 = resist.Embed(title="resist", icon_url="abc")

        assert e1 == resist.Embed.from_api(data)

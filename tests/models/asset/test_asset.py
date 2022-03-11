from __future__ import annotations

import resist


class TestAsset:
    def test_attributes(self) -> None:
        avatar = resist.Asset(
            {  # type: ignore
                "_id": "foo",
                "tag": "bar",
                "size": 1,
                "filename": "baz",
                "metadata": {},
                "content_type": "qux",
            }
        )

        assert avatar.unique == "foo"
        assert avatar.tag == "bar"
        assert avatar.size == 1  # type: ignore
        assert avatar.filename == "baz"  # type: ignore
        assert avatar.metadata == {}  # type: ignore
        assert avatar.content_type == "qux"  # type: ignore

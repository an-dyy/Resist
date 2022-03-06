from __future__ import annotations

import pytest

import resist


class TestRelationship:
    @pytest.fixture()
    def relationship(self) -> resist.Relationship:
        return resist.Relationship({"_id": "foo", "status": "Blocked"})

    def test_attributes(self, relationship: resist.Relationship) -> None:
        assert relationship.unique == "foo"
        assert relationship.status == "Blocked"
        assert relationship.data == {"_id": "foo", "status": "Blocked"}

from __future__ import annotations

from typing import Literal

import attr

from ...types import RelationData

__all__ = ("Relationship",)


@attr.s(slots=True)
class Relationship:
    """Represents a relationship.

    Attributes
    ----------
    unique: :class:`str`
        The ID of the other user.

    status: :class:`str`
        The status of your relationship.
    """

    data: RelationData = attr.field(repr=False)

    unique: str = attr.field(init=False, repr=True)
    status: Literal[
        "Blocked", "BlockedOther", "Friend", "Incoming", "None", "Outgoing", "User"
    ] = attr.field(init=False, repr=True)

    def __attrs_post_init__(self) -> None:
        self.unique = self.data["_id"]
        self.status = self.data["status"]

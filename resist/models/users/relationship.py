from __future__ import annotations

from typing import Literal

from attrs import define, field

from ...types import RelationData

__all__ = ("Relationship",)


@define
class Relationship:
    """Represents a relationship.

    Attributes
    ----------
    unique: :class:`str`
        The ID of the other user.

    status: :class:`str`
        The status of your relationship.
    """

    data: RelationData = field(repr=False)

    unique: str = field(init=False, repr=True)
    status: Literal[
        "Blocked", "BlockedOther", "Friend", "Incoming", "None", "Outgoing", "User"
    ] = field(init=False, repr=True)

    def __attrs_post_init__(self) -> None:
        self.unique = self.data["_id"]
        self.status = self.data["status"]

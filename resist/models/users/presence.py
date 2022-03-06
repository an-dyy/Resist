from __future__ import annotations

from typing import Literal

import attr

from ...types import StatusData

__all__ = ("Presence",)


@attr.s(slots=True)
class Presence:
    """Represents presence.

    Attributes
    ----------
    text: None | :class:`str`
        Custom status text.

    presence: None | :class:`str`
        The presence of the user.
    """

    data: StatusData = attr.field(repr=False)

    text: None | str = attr.field(init=False, repr=True)
    kind: None | Literal["Busy", "Idle", "Invisible", "Online"] = attr.field(
        init=False, repr=True
    )

    def __attrs_post_init__(self) -> None:
        self.text = self.data.get("text")
        self.kind = self.data.get("presence")

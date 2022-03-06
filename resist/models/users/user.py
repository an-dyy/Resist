from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import attr
from typing_extensions import Self

from ...types import UserData
from ..assets import Avatar
from ..cacheable import Cacheable
from ..fetchable import Fetchable
from .flags import UserBadges, UserFlags
from .presence import Presence
from .relationship import Relationship

if TYPE_CHECKING:
    from ...client import WebSocketClient

__all__ = ("User",)


@attr.s(slots=True)
class User(Cacheable, Fetchable):
    """A class representing a User object.

    Attributes
    ----------
    client: :class:`.WebSocketClient`
        The client used for this user.

    data: :class:`dict`
        The raw data of the user retreived from the API.

    unique: :class:`str`
        The unique ID of the user.

    username: :class:`str`
        The username of the user.

    avatar: None | :class:`.Avatar`
        The avatar of the user.

    relations: :class:`list`
        A list of :class:`.Relationship` for the user.

    badges: :class:`.UserBadges`
        The user's badges.

    presence: None | :class:`.Presence`
        The presence of the user.

    online: :class:`bool`
        If the user is currently online.

    bot: :class:`bool`
        If the user is a bot.

    owner: None | :class:`str`
        The ID of the owner, this is given when the user is a bot.

    flags: :class:`.UserFlags`
        The user's flags.

    relationship: None | :class:`str`
        The relationship you have with this user.
    """

    client: WebSocketClient = attr.field(repr=False)
    data: UserData = attr.field(repr=False)

    unique: str = attr.field(init=False, repr=True)
    username: str = attr.field(init=False, repr=True)
    avatar: None | Avatar = attr.field(init=False, repr=False)

    relations: list[Relationship] = attr.field(init=False, repr=False)
    badges: UserBadges = attr.field(init=False, repr=True)
    presence: None | Presence = attr.field(init=False, repr=True)

    online: bool = attr.field(init=False, repr=True)
    bot: bool = attr.field(init=False, repr=True)
    owner: None | str = attr.field(init=False, repr=True)
    flags: UserFlags = attr.field(init=False, repr=True)

    relationship: None | Literal[
        "Blocked", "BlockedOther", "Friend", "Incoming", "None", "Outgoing", "User"
    ] = attr.field(init=False, repr=True)

    def __attrs_post_init__(self) -> None:
        self.unique = self.data["_id"]
        self.username = self.data["username"]

        self.avatar = None
        if avatar_data := self.data.get("avatar"):
            self.avatar = Avatar(avatar_data)

        self.relations = []
        if relations_data := self.data.get("relations"):
            self.relations = [Relationship(r) for r in relations_data]

        self.badges = UserBadges(self.data.get("badges", 0))

        self.presence = None
        if presence_data := self.data.get("presence"):
            self.presence = Presence(presence_data)

        self.online = self.data.get("online", False)

        self.bot = False
        self.owner = None
        if bot_data := self.data.get("bot"):
            self.owner = bot_data["owner"]
            self.bot = True

        self.flags = UserFlags(self.data.get("flags", 0))
        self.relationship = self.data.get("relationship")

    @classmethod
    async def fetch(cls: type[Self], client: WebSocketClient, unique: str) -> Self:
        """Fetches the user of the given ID.

        Parameters
        ----------
        client: :class:`.WebSocketClient`
            The client to use for this user.

        unique: :class:`str`
            The unique ID of the user.

        Returns
        -------
        :class:`.User`
            The user fetched.
        """
        return cls(client, await client.rest.request("GET", f"users/{unique}"))

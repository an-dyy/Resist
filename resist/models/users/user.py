from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from attrs import define, field
from typing_extensions import Self

from ...types import UserData
from ..assets import Asset
from ..cacheable import Cacheable
from ..fetchable import Fetchable
from .flags import UserBadges, UserFlags
from .presence import Presence
from .relationship import Relationship

if TYPE_CHECKING:
    from ...client import WebSocketClient

__all__ = ("User",)


@define
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

    avatar: None | :class:`.Asset`
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

    client: WebSocketClient = field(repr=False)
    data: UserData = field(repr=False)

    unique: str = field(init=False, repr=True)
    username: str = field(init=False, repr=True)
    avatar: None | Asset = field(init=False, repr=False)

    relations: list[Relationship] = field(init=False, repr=False)
    badges: UserBadges = field(init=False, repr=True)
    presence: None | Presence = field(init=False, repr=True)

    online: bool = field(init=False, repr=True)
    bot: bool = field(init=False, repr=True)
    owner: None | str = field(init=False, repr=True)
    flags: UserFlags = field(init=False, repr=True)

    relationship: None | Literal[
        "Blocked", "BlockedOther", "Friend", "Incoming", "None", "Outgoing", "User"
    ] = field(init=False, repr=True)

    def __attrs_post_init__(self) -> None:
        self.unique = self.data["_id"]
        self.username = self.data["username"]

        self.avatar = None
        if avatar_data := self.data.get("avatar"):
            self.avatar = Asset(avatar_data)

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

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, cast

from attrs import define, field

from ..types import MasqueradeData, MessageData
from .assets import Asset
from .cacheable import Cacheable
from .embed import Embed
from .fetchable import Fetchable

if TYPE_CHECKING:
    from ..client import WebSocketClient


__all__ = ("Message",)


@define
class Message(Cacheable, Fetchable):
    """Represents a message sent on Revolt.

    Attributes
    ----------
    client: :class:`.WebSocketClient`
        The client used for this user.

    data: :class:`dict`
        The raw data of the message.

    unique: :class:`str`
        The unique ID of the message.

    nonce: None | :class:`str`
        Nonce value.

    channel: :class:`str`
        The channel in which the message was sent.

    author: :class:`str`
        The user who sent this message.

    content: :class:`str`
        The message content.

    attachments: :class:`list[.Asset]`
        List of attachments in this message.

    edited_at: :class:`datetime.datetime`
        Timestamp at which this message was edited at.

    embeds: :class:`list[.Embed]`
        List of embeds sent in this message.

    mentions: :class:`list[str]`
        The list of members mentioned in this message.

    replies: :class:`list[.Message]`
        The list of messages being replied to.

    relationship: None | :class:`dict`
        Alternate username/avatar used while sending this message.
    """

    client: WebSocketClient = field(repr=False)
    data: MessageData = field(repr=False)

    unique: str = field(init=False, repr=True)
    nonce: str | None = field(init=False, repr=True)
    channel: str = field(
        init=False, repr=True
    )  # TODO: change this to a full Channel object
    author: str = field(
        init=False, repr=True
    )  # TODO: change this to a full Member object
    content: str = field(init=False, repr=True)
    attachments: list[Asset] = field(init=False, repr=True)
    edited_at: datetime | None = field(init=False, repr=True)
    embeds: list[Embed] = field(init=False, repr=True)
    mentions: list[str] = field(
        init=False, repr=True
    )  # TODO: change this to list[Member]
    replies: list[Message] = field(init=False, repr=True)
    masquerade: MasqueradeData | None = field(init=False, repr=True)

    def __attrs_post_init__(self) -> None:
        self.unique = self.data["_id"]
        self.nonce = self.data.get("nonce")
        self.channel = self.data["channel"]
        self.author = self.data["author"]
        self.content = cast(str, self.data["content"])
        self.attachments = [Asset(i) for i in self.data.get("attachments", [])]

        if edited := self.data.get("edited"):
            self.edited_at = datetime.fromisoformat(edited["$date"])
        else:
            self.edited_at = None

        self.embeds = [Embed.from_api(i) for i in self.data.get("embeds", [])]
        self.mentions = self.data.get("mentions", [])
        self.replies = [Message.cache[id] for id in self.data.get("replies", [])]
        self.masquerade = self.data.get("masquerade")

        Message.cache.set(self.unique, self)

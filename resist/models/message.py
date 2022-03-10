from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from attrs import define, field

from ..types import (
    ChannelActionSystemMessageContent,
    MasqueradeData,
    MessageData,
    SystemMessageContent,
    UserActionSystemMessageContent,
)
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

    masquerade: None | :class:`dict`
        Alternate username/avatar used while sending this message.

    system: None | :class:`dict`
        Contains additional information about the message, if it
        was sent by a system user.
        This attribute is None for non-system messages.
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
    system: (
        SystemMessageContent
        | UserActionSystemMessageContent
        | ChannelActionSystemMessageContent
        | None
    ) = field(init=False, repr=True)

    def __attrs_post_init__(self) -> None:
        self.unique = self.data["_id"]
        self.nonce = self.data.get("nonce")
        self.channel = self.data["channel"]
        self.author = self.data["author"]

        content = self.data["content"]

        if isinstance(content, str):
            self.content = content
            self.system = None
        else:
            self.content = self._handle_system_message_content(content)
            self.system = content

        self.attachments = [Asset(i) for i in self.data.get("attachments", [])]

        if edited := self.data.get("edited"):
            self.edited_at = datetime.strptime(edited["$date"], "%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            self.edited_at = None

        self.embeds = [Embed.from_api(i) for i in self.data.get("embeds", [])]
        self.mentions = self.data.get("mentions", [])
        self.replies = [Message.cache[id] for id in self.data.get("replies", [])]
        self.masquerade = self.data.get("masquerade")

        Message.cache.set(self.unique, self)

    @staticmethod
    def _handle_system_message_content(
        data: SystemMessageContent
        | UserActionSystemMessageContent
        | ChannelActionSystemMessageContent,
    ) -> str:
        # In the case of system messages, the "content" field in the API respomse
        # is a dictionary whose varies according to the type of the system message.
        # However, annotating Message.content to a Union will make using it quite painful
        # to use, needing casts and unnecessary type narrowing.
        # Moreover, the number of system messages is negligble in comparison
        # to normal text messages, so to avoid this union type, we
        # extract a pseudo "content" from the system message dictionary
        if data["type"] == "text":
            # type of data is SystemMessageContent
            return data["content"]
        elif "id" in data:
            # type of data is UserActionSystemMessageContent
            return f"type:{data['type']} id:{data['id']}"
        else:
            return f"type:{data['type']} by:{data['by']}"

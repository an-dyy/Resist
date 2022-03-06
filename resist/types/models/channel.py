from __future__ import annotations

from typing import Literal, TypedDict

from typing_extensions import NotRequired

__all__ = (
    "MetaData",
    "MediaMetaData",
    "IconData",
    "SavedMessagesData",
    "DirectMessagesData",
    "GroupData",
    "TextChannelData",
    "VoiceChannelData",
)


class MetaData(TypedDict):
    type: Literal["File", "Text", "Audio"]


class MediaMetaData(TypedDict):
    type: Literal["Image", "Video"]
    width: int
    height: int


class IconData(TypedDict):
    _id: str
    tag: Literal["attachments", "avatars", "backgrounds", "banners", "icons"]
    size: int
    filename: str
    metadata: MetaData | MediaMetaData
    content_type: str


class SavedMessagesData(TypedDict):
    _id: str
    channel_type: Literal["SavedMessages"]
    user: str


class DirectMessagesData(TypedDict):
    _id: str
    channel_type: Literal["DirectMessages"]
    active: bool
    recipients: list[str]
    last_message_id: NotRequired[str]


class GroupData(TypedDict):
    _id: str
    channel_type: Literal["Group"]
    recipients: list[str]
    name: str
    owner: str

    description: NotRequired[str]
    last_message_id: NotRequired[str]
    icon: NotRequired[IconData]

    permissions: NotRequired[int]
    nsfw: NotRequired[bool]


class TextChannelData(TypedDict):
    _id: str
    server: str
    name: str

    description: NotRequired[str]
    icon: NotRequired[IconData]

    default_permissions: NotRequired[int]
    role_permissions: NotRequired[int]
    nsfw: NotRequired[bool]

    channel_type: Literal["TextChannel"]
    last_message_id: NotRequired[str]


class VoiceChannelData(TypedDict):
    _id: str
    server: str
    name: str

    description: NotRequired[str]
    icon: NotRequired[IconData]

    default_permissions: NotRequired[int]
    role_permissions: NotRequired[int]
    nsfw: NotRequired[bool]

    channel_type: Literal["VoiceChannel"]

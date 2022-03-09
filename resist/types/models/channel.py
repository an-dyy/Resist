from __future__ import annotations

from typing import Literal, TypedDict

from typing_extensions import NotRequired

from .asset import AssetData


__all__ = (
    "SavedMessagesData",
    "DirectMessagesData",
    "GroupData",
    "TextChannelData",
    "VoiceChannelData",
)


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
    icon: NotRequired[AssetData]

    permissions: NotRequired[int]
    nsfw: NotRequired[bool]


class TextChannelData(TypedDict):
    _id: str
    server: str
    name: str

    description: NotRequired[str]
    icon: NotRequired[AssetData]

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
    icon: NotRequired[AssetData]

    default_permissions: NotRequired[int]
    role_permissions: NotRequired[int]
    nsfw: NotRequired[bool]

    channel_type: Literal["VoiceChannel"]

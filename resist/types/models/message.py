from __future__ import annotations

from typing import Literal, TypedDict, Union

from typing_extensions import NotRequired

from .attachments import AttachmentData


class YoutubeLinkEmbedMetadata(TypedDict):
    type: Literal["YouTube"]
    id: str
    timestamp: NotRequired[str]


class TwitchLinkEmbedMetadata(TypedDict):
    type: Literal["Twitch"]
    content_type: Literal["Channel", "Clip", "Video"]
    id: str


class SpotifyLinkEmbedMetadata(TypedDict):
    type: Literal["Spotify"]
    content_type: str
    id: str


SoundcloudLinkEmbedMetadata = TypedDict(
    "SoundcloudLinkEmbedMetadata", {"type": Literal["Soundcloud"]}
)


class BandcampLinkEmbedMetadata(TypedDict):
    type: Literal["Bandcamp"]
    content_type: Literal["Album", "Track"]
    id: str


class EmbedMediaData(TypedDict):
    # base fields that both videos and images sent in embeds will have.
    url: str
    width: int
    height: int


class EmbedImageData(EmbedMediaData):
    # this contains the data about an image sent in an embed
    # for example: a banner image in a URL's embed
    size: Literal["Large", "Preview"]


class WebsiteEmbedData(TypedDict):
    """Represents the data of an embed for a URL."""

    type: Literal["Website"]
    url: NotRequired[str]
    special: NotRequired[
        YoutubeLinkEmbedMetadata
        | SpotifyLinkEmbedMetadata
        | TwitchLinkEmbedMetadata
        | SoundcloudLinkEmbedMetadata
        | BandcampLinkEmbedMetadata
    ]
    title: NotRequired[str]
    description: NotRequired[str]
    image: NotRequired[EmbedImageData]
    video: NotRequired[EmbedMediaData]
    site_name: NotRequired[str]
    icon_url: NotRequired[str]
    colour: NotRequired[str]


class ImageEmbedData(EmbedImageData):
    """Represents the data of an image embed."""

    type: Literal["Image"]


class TextEmbedData(TypedDict):
    type: Literal["Text"]
    icon_url: NotRequired[str]
    url: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    media: NotRequired[AttachmentData]
    colour: NotRequired[str]


NoneEmbed = TypedDict("NoneEmbed", {"type": Literal["None"]})


class SystemMessageContent(TypedDict):
    type: Literal["text"]
    content: str


class UserActionSystemMessageContent(TypedDict):
    type: Literal[
        "user_added",
        "user_remove",
        "user_joined",
        "user_left",
        "user_kicked",
        "user_banned",
    ]
    id: str
    by: NotRequired[str]  # sent only with user_added and user_remove


class ChannelActionSystemMessageContent(TypedDict):
    type: Literal[
        "channel_renamed", "channel_description_changed", "channel_icon_changed"
    ]
    by: str
    name: NotRequired[str]  # sent only with channel_renamed


MessageEditedData = TypedDict("MessageEditedData", {"$date": str})


class MasqueradeData(TypedDict):
    name: NotRequired[str]
    avatar: NotRequired[str]


EmbedType = Union[WebsiteEmbedData, ImageEmbedData, TextEmbedData, NoneEmbed]


class MessageData(TypedDict):
    _id: str
    nonce: NotRequired[str]
    channel: str
    author: str
    content: (
        SystemMessageContent
        | UserActionSystemMessageContent
        | ChannelActionSystemMessageContent
        | str
    )
    attachments: NotRequired[list[AttachmentData]]
    edited: NotRequired[MessageEditedData]
    embeds: NotRequired[EmbedType]
    mentions: NotRequired[list[str]]
    replies: NotRequired[list[str]]
    masquerade: NotRequired[MasqueradeData]

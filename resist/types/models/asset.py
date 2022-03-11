from __future__ import annotations

from typing import Literal, TypedDict


__all__ = ("MetaData", "MediaMetaData", "AssetData")


class MetaData(TypedDict):
    type: Literal["File", "Text", "Audio"]


class MediaMetaData(TypedDict):
    type: Literal["Image", "Video"]
    width: int
    height: int


class AssetData(TypedDict):
    _id: str
    tag: Literal["attachments", "avatars", "backgrounds", "banners", "icons"]
    size: int
    filename: str
    metadata: MetaData | MediaMetaData
    content_type: str

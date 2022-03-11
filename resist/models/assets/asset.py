from __future__ import annotations

from typing import Literal

from attrs import define, field

from ...types import AssetData, MediaMetaData, MetaData


@define
class Asset:
    """Represents an Asset, like an avatar or an attachment.

    Attributes
    ----------
    unique: :class:`str`
        The asset identifier.

    size: :class:`int`
        Size of the asset in bytes.

    filename: :class:`str`
        The name of the file.

    metadata: :class:`dict`
        The metadata of the asset.

    content_type: :class:`str`
        The MIME type of the asset.

    tag: :class:`str`
        The tag of the asset.
        Could be one of "attachments", "avatars", "backgrounds", "banners" and "icons".
    """

    data: AssetData = field(init=True, repr=False)

    unique: str = field(init=False, repr=True)
    tag: Literal["attachments", "avatars", "backgrounds", "banners", "icons"] = field(
        init=False, repr=True
    )
    size: int = field(init=False, repr=True)
    filename: str = field(init=False, repr=True)
    metadata: MetaData | MediaMetaData = field(init=False, repr=True)
    content_type: str = field(init=False, repr=True)

    def __attrs_post_init__(self) -> None:
        self.unique = self.data["_id"]
        self.tag = self.data["tag"]
        self.size = self.data["size"]
        self.filename = self.data["filename"]
        self.metadata = self.data["metadata"]
        self.content_type = self.data["content_type"]

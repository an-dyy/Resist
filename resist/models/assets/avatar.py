from __future__ import annotations

from typing import Literal

import attr

from ...types import AttachmentData, MediaMetaData, MetaData

__all__ = ("Avatar",)


@attr.s(slots=True)
class Avatar:
    """Represents an avatar.

    Attributes
    ----------
    unique: :class:`str`
        The Avatar identifier.

    size: :class:`int`
        Size of the image in bytes.

    filename: :class:`str`
        The name of the file.

    metadata: :class:`dict`
        The metadata of the avatar.

    content_type: :class:`str`
        The MIME type of the avatar.

    tag: :class:`str`
        The tag of the avatar.
    """

    data: AttachmentData = attr.field(repr=False)

    unique: str = attr.field(init=False, repr=True)
    size: int = attr.field(init=False, repr=True)
    filename: str = attr.field(init=False, repr=True)
    metadata: MetaData | MediaMetaData = attr.field(init=False, repr=True)
    content_type: str = attr.field(init=False, repr=True)

    tag: Literal[
        "attachments", "avatars", "backgrounds", "banners", "icons"
    ] = attr.field(init=False, repr=True)

    def __attrs_post_init__(self) -> None:
        self.unique = self.data["_id"]
        self.tag = self.data["tag"]
        self.size = self.data["size"]
        self.filename = self.data["filename"]
        self.metadata = self.data["metadata"]
        self.content_type = self.data["content_type"]

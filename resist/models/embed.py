from __future__ import annotations

from typing import Type
from typing_extensions import Self

from attrs import define, field

from ..models.assets import Asset

from ..types import EmbedType as EmbedData


@define
class Embed:
    """Represents an embed.

    Attributes
    ----------
    title: None | :class:`str`
        The title of the embed.

    url: None | :class:`str`
        The URL of the embed.

    description: None | :class:`str`
        The description of the embed.

    icon_url: None | :class:`str`
        URL to the embed's icon.

    media: None | :class:`.Asset`
        The media that was sent in the embed.

    colour: None | :class:`str`
        The embed's colour.

    data: :class:`dict`
        The embed's raw data.
    """

    title: str | None = field(init=True, repr=True, default=None, kw_only=True)
    url: str | None = field(init=True, repr=True, default=None, kw_only=True)
    description: str | None = field(init=True, repr=True, default=None, kw_only=True)
    icon_url: str | None = field(init=True, repr=True, default=None, kw_only=True)
    media: Asset | None = field(init=True, repr=True, default=None, kw_only=True)
    colour: str | None = field(init=True, repr=True, default=None, kw_only=True)
    data: EmbedData = field(init=True, repr=False, default=None, kw_only=True)

    def __attrs_post_init__(self) -> None:
        if self.data is not None:
            # instance created by the API will have non-empty data attribute
            self.title = self.data.get("title")
            self.url = self.data.get("url")
            self.description = self.data.get("description")
            self.icon_url = self.data.get("icon_url")

            if media := self.data.get("media"):
                self.media = Asset(media)
            self.colour = self.data.get("colour")
            return

        # instance created by user will have empty data attribute, so construct it here
        self.data = {"type": "Text"}
        if title := self.title:
            self.data["title"] = title
        if url := self.url:
            self.data["url"] = url
        if description := self.description:
            self.data["description"] = description
        if icon_url := self.icon_url:
            self.data["icon_url"] = icon_url
        if media := self.media:
            self.data["media"] = media.data
        if colour := self.colour:
            self.data["colour"] = colour

    @classmethod
    def from_api(cls: Type[Self], data: EmbedData) -> Self:
        return Embed(data=data)

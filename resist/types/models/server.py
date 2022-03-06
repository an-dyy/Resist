from __future__ import annotations

from typing import TypedDict

from typing_extensions import NotRequired

from .channel import IconData

__all__ = ("CategoryData", "SystemMessagesData", "RoleData", "ServerData")


class CategoryData(TypedDict):
    id: str
    title: str
    channels: str


class SystemMessagesData(TypedDict):
    user_joined: NotRequired[str]
    user_left: NotRequired[str]

    user_Kicked: NotRequired[str]
    user_banned: NotRequired[str]


class RoleData(TypedDict):
    name: str
    permissions: str

    colour: NotRequired[str]
    hoist: NotRequired[bool]
    rank: NotRequired[int]


class ServerData(TypedDict):
    _id: str
    owner: str
    name: str
    description: NotRequired[str]

    channels: list[str]
    categories: NotRequired[list[CategoryData]]
    system_messages: NotRequired[list[SystemMessagesData]]
    roles: NotRequired[list[RoleData]]
    default_permissions: list[tuple[int, int]]

    icon: NotRequired[IconData]
    banner: NotRequired[IconData]
    nsfw: NotRequired[bool]
    flags: NotRequired[int]
    analytics: NotRequired[bool]
    discoverable: NotRequired[bool]

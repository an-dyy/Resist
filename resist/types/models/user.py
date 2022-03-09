from __future__ import annotations

from typing import Literal, TypedDict

from typing_extensions import NotRequired

from .attachments import AttachmentData

__all__ = ("RelationData", "StatusData", "BotData", "UserData")


class RelationData(TypedDict):
    _id: str

    status: Literal[
        "Blocked", "BlockedOther", "Friend", "Incoming", "None", "Outgoing", "User"
    ]


class StatusData(TypedDict):
    text: NotRequired[str]
    presence: NotRequired[Literal["Busy", "Idle", "Invisible", "Online"]]


class BotData(TypedDict):
    owner: str


class UserData(TypedDict):
    _id: str
    username: str

    avatar: NotRequired[AttachmentData]
    relations: NotRequired[list[RelationData]]

    badges: NotRequired[int]
    status: NotRequired[StatusData]

    relationship: NotRequired[
        Literal[
            "Blocked", "BlockedOther", "Friend", "Incoming", "None", "Outgoing", "User"
        ]
    ]

    online: NotRequired[bool]
    flags: NotRequired[int]
    bot: NotRequired[BotData]

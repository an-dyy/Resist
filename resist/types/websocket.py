from __future__ import annotations

from typing import TypedDict

from .models import (
    DirectMessagesData,
    GroupData,
    SavedMessagesData,
    ServerData,
    TextChannelData,
    UserData,
    VoiceChannelData,
)

__all__ = ("Auth", "Error", "Authenticated", "Pong", "Ready")


class Auth(TypedDict):
    type: str
    token: str


class Error(TypedDict):
    type: str
    error: str


class Authenticated(TypedDict):
    type: str


class Pong(TypedDict):
    type: str
    data: int


class Ready(TypedDict):
    type: str
    users: list[UserData]
    servers: list[ServerData]
    channels: list[
        SavedMessagesData
        | DirectMessagesData
        | GroupData
        | TextChannelData
        | VoiceChannelData
    ]

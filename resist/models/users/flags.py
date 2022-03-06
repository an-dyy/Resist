from __future__ import annotations

from ..flags import Flag

__all__ = ("UserBadges", "UserFlags")


class UserBadges(Flag):
    """The user's badges."""

    developer = 1 << 0
    translator = 1 << 1
    supporter = 1 << 2
    responsible_disclosure = 1 << 3
    founder = 1 << 4
    platform_moderation = 1 << 5
    active_supporter = 1 << 6
    paw = 1 << 7
    early_adopter = 1 << 8
    reversed_relevant_joke = 1 << 9


class UserFlags(Flag):
    """The user's flags."""

    suspended = 1 << 0
    deleted = 1 << 1
    banned = 1 << 2

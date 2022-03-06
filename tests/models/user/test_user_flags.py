from __future__ import annotations

import resist


class TestUserBadges:
    def test_values(self) -> None:
        assert resist.UserBadges(1).developer is True
        assert resist.UserBadges(2).translator is True
        assert resist.UserBadges(4).supporter is True
        assert resist.UserBadges(8).responsible_disclosure is True
        assert resist.UserBadges(16).founder is True
        assert resist.UserBadges(32).platform_moderation is True
        assert resist.UserBadges(64).active_supporter is True
        assert resist.UserBadges(128).paw is True
        assert resist.UserBadges(256).early_adopter is True
        assert resist.UserBadges(512).reversed_relevant_joke is True


class TestUserFlags:
    def test_values(self) -> None:
        assert resist.UserFlags(1).suspended is True
        assert resist.UserFlags(2).deleted is True
        assert resist.UserFlags(4).banned is True

from __future__ import annotations

from typing import TypedDict

__all__ = (
    "Feature",
    "CaptchaFeature",
    "MonthFeature",
    "VosoFeature",
    "Features",
    "APIContext",
)


class Feature(TypedDict):
    enabled: bool


class CaptchaFeature(Feature):
    enabled: bool
    key: str


class MonthFeature(Feature):
    enabled: bool
    url: str


class VosoFeature(Feature):
    enabled: bool
    url: str
    ws: str


class Features(TypedDict):
    captcha: CaptchaFeature
    email: bool
    invite_only: bool
    autumn: MonthFeature
    january: MonthFeature
    voso: VosoFeature


class APIContext(TypedDict):
    revolt: str
    features: Features
    ws: str
    app: str
    vapid: str

from __future__ import annotations

from typing import Any, Iterator, TypeVar

__all__ = ("Flag",)

FlagT = TypeVar("FlagT", bound="Flag")


class InvalidFlag(TypeError):
    def __init__(self, name: str, flag: type[Flag]) -> None:
        self.valid_flags: tuple[str, ...] = tuple(flag.__members__.keys())
        self.name = name
        self.flag = flag

        super().__init__(f"{name!r} is not a valid flag for {flag.__name__}")


class FlagValue(int):
    _name_: str
    _value_: int

    def __new__(cls, name: str, value: int):
        obj = super().__new__(cls, value)

        obj._name_ = name
        obj._value_ = value

        return obj

    def __repr__(self) -> str:
        return f"<FlagValue name={self.name!r} value={self.value}>"

    @property
    def name(self) -> str:
        return self._name_

    @property
    def value(self) -> int:
        return self._value_


class FlagMeta(type):
    __members__: dict[str, FlagValue]

    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        members: dict[str, FlagValue] = {}

        for attr, value in attrs.copy().items():
            is_method = callable(value) or isinstance(value, (staticmethod, classmethod))

            if not attr.startswith(("__", "_")) and not is_method:
                members[attr] = FlagValue(attr, value)  # type: ignore
                del attrs[attr]

        attrs["__members__"] = members
        return super().__new__(cls, name, bases, attrs)

    def __getattr__(cls, name: str) -> FlagValue:
        value = cls.__members__.get(name)
        if not value:
            raise AttributeError(f"{cls.__name__} has no attribute {name!r}")

        return value

    def __iter__(self):
        return iter(self.__members__.values())


class Flag(metaclass=FlagMeta):
    __members__: dict[str, FlagValue]
    value: int

    def __init__(self, value: int = 0, **kwargs: bool) -> None:
        self.value = value
        cls = type(self)

        for name, value in kwargs.items():
            flag: None | FlagValue = getattr(cls, name, None)
            if not flag:
                raise InvalidFlag(name, cls)

            if self.value & flag:
                continue

            if value is True:
                self.value |= flag
            else:
                self.value &= ~flag

    def __getattr__(self, name: str) -> bool:
        if flag := self.__members__.get(name):
            return bool(self.value & flag.value)

        raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")

    def __setattr__(self, name: str, value: Any) -> None:
        flag = self.__members__.get(name)
        if not flag:
            return super().__setattr__(name, value)

        if self.value & flag:
            return

        if value:
            self.value |= flag
        else:
            self.value &= ~flag

    def __iter__(self) -> Iterator[Any]:
        return iter(self.__values__.items())

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} value={self.value}>"

    def __or__(self: FlagT, other: int | FlagT) -> FlagT:
        if isinstance(other, int):
            return self.__class__(self.value | other)

        return self.__class__(self.value | other.value)

    def __and__(self: FlagT, other: int | FlagT) -> FlagT:
        if isinstance(other, int):
            return self.__class__(self.value & other)

        return self.__class__(self.value & other.value)

    def __invert__(self: FlagT) -> FlagT:
        return self.__class__(~self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __eq__(self: FlagT, other: FlagT) -> bool:  # type: ignore
        if not isinstance(other, Flag):
            return NotImplemented

        return self.value == other.value

    @property
    def __values__(self) -> dict[FlagValue, bool]:
        return {flag: bool(self.value & flag.value) for flag in self.__class__}

from __future__ import annotations

from typing import Any, Generic, TypeVar

import attr
from typing_extensions import Self

__all__ = ("Cache", "Cacheable")

KeyT = TypeVar("KeyT")
ValueT = TypeVar("ValueT")


@attr.s(slots=True)
class Cache(Generic[KeyT, ValueT]):
    """A class which handles in-memory caching.

    .. note::

        All cache-able classes have this class under the attribute `Class.cache`

    Parameters
    ----------
    max: None | :class:`int`
        The max amount of keys allowed in the cache.

    Attributes
    ----------
    root: :class:`dict`
        The internal dict of the cache.

    max_items: None | :class:`int`
        The max amount of items the cache can have at a given time.

    len: :class:`int`
        The current amount of items in the cache.
    """

    root: dict[KeyT, ValueT] = attr.field(init=False, repr=False)
    len: int = attr.field(init=False, default=0)
    max_items: None | int = attr.field(repr=True)

    def __attrs_post_init__(self) -> None:
        self.root: dict[KeyT, ValueT] = {}

    def __setitem__(self, key: KeyT, value: ValueT) -> None:
        self.root[key] = value
        self.len += 1

        if self.max_items is not None and self.len > self.max_items:
            self.pop()

    def __getitem__(self, key: KeyT) -> ValueT:
        return self.root[key]

    def set(self, key: KeyT, value: ValueT) -> None:
        """Sets a key-value pair in the cache.

        Parameters
        ----------
        key: Any
            The key to use.

        value: Any
            The value of the key.
        """
        return self.__setitem__(key, value)

    def get(self, key: KeyT) -> None | ValueT:
        """Grabs from the cache.

        Parameters
        ----------
        key: Any
            The key to query with.

        Returns
        -------
        None | Any
            The item grabbed from the cache.
        """
        return self.root.get(key)

    def pop(self, key: None | KeyT = None) -> ValueT:
        """Pops a key from the cache.
        If no key is given, pop the first inserted key.

        Parameters
        ----------
        key: None | Any
            The key to pop.

        Returns
        -------
        Any
            The value of the key popped.
        """
        self.len -= 1

        if key is not None:
            return self.root.pop(key)

        return self.root.pop(list(self.root.keys())[0])


class Cacheable:
    """Represents a cache-able model.

    Attributes
    ----------
    cache: :class:`.Cache`
        The cache for this model.
    """

    __cache__: Cache[Any, Self]

    def __init_subclass__(cls: type[Self], **kwargs: Any) -> None:
        cls.__cache__ = Cache[Any, Self](kwargs.get("max_items"))

    @classmethod
    @property
    def cache(cls: type[Self]) -> Cache[Any, Self]:
        return cls.__cache__

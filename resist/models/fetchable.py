from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from typing_extensions import Self

if TYPE_CHECKING:
    from ..client import WebSocketClient

__all__ = ("Fetchable",)


@runtime_checkable
class Fetchable(Protocol):
    """A fetch-able base class.

    This class should be inherited by any class
    which can be fetched from the API. Must require the unique id.

    Attributes
    ----------
    unique: :class:`str`
        The unique identifier of the model.
    """

    __slots__ = ()
    unique: str

    @classmethod
    async def fetch(cls: type[Self], client: WebSocketClient, unique: str) -> Self:
        """Makes an API call to fetch the model by it's ID.

        Parameters
        ----------
        unique: :class:`str`
            The unique ID to fetch with.

        Returns
        -------
        :class:`.Fetchable`
            The model fetched.
        """
        raise NotImplementedError

from __future__ import annotations

import pytest

import resist


class TestFetchable:
    class Model(resist.Fetchable):
        ...

    @pytest.fixture()
    def model(self) -> type[Model]:
        return TestFetchable.Model

    def test_attributes(self, model: type[Model]) -> None:
        assert hasattr(model, "__slots__")
        assert hasattr(model, "fetch")
        assert not hasattr(model, "unique")

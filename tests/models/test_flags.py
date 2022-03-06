from __future__ import annotations

import pytest

import resist


class TestFlag:
    class Test(resist.Flag):
        foo = 1 << 0
        bar = 1 << 1
        baz = 1 << 2
        qux = 1 << 3

    @pytest.fixture()
    def flag(self) -> type[Test]:
        return TestFlag.Test

    def test_values(self, flag: type[TestFlag.Test]) -> None:
        test = flag(4)

        assert test.foo is False
        assert test.bar is False
        assert test.baz is True
        assert test.qux is False

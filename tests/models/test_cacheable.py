from __future__ import annotations

import pytest

import resist


class TestCache:
    @pytest.fixture()
    def cache(self) -> resist.Cache[int, str]:
        return resist.Cache[int, str](5)

    def test_attributes(self, cache: resist.Cache[int, str]) -> None:
        assert cache.max_items == 5
        assert cache.len == 0
        assert cache.root == {}

    def test_set(self, cache: resist.Cache[int, str]) -> None:
        cache.set(1, "foo")
        cache.set(2, "bar")
        cache.set(3, "baz")
        cache.set(4, "qux")

        assert cache.len == 4
        assert cache.root == {1: "foo", 2: "bar", 3: "baz", 4: "qux"}

    def test_get(self, cache: resist.Cache[int, str]) -> None:
        cache.set(1, "foo")
        bar = cache.get(2)

        assert cache.get(1) == "foo"
        assert bar is None

    def test_pop(self, cache: resist.Cache[int, str]) -> None:
        cache.set(1, "foo")
        cache.set(2, "bar")
        cache.set(3, "baz")

        assert cache.pop(1) == "foo"
        assert cache.pop(2) == "bar"
        assert cache.pop() == "baz"
        assert cache.len == 0
        assert cache.root == {}

        cache.set(1, "foo")
        cache.set(2, "bar")
        cache.set(3, "baz")

        assert cache.pop() == "foo"
        [cache.pop() for _ in range(2)]

        with pytest.raises(IndexError):

            cache.pop()

    def test_max_items(self, cache: resist.Cache[int, str]) -> None:
        [cache.set(i, str(i)) for i in range(20)]

        assert cache.len == 5
        assert len(cache.root) == 5


class TestCacheable:
    class Model(resist.Cacheable, max_items=5):
        ...

    @pytest.fixture()
    def cache(self) -> type[Model]:
        return TestCacheable.Model

    def test_attributes(self, cache: type[Model]) -> None:
        assert hasattr(cache, "cache")
        assert hasattr(cache, "__cache__")

        assert cache.cache.max_items == 5

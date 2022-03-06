from __future__ import annotations

import asyncio
from datetime import timedelta
from unittest import mock

import pytest

import resist


class TestEvents:
    @pytest.fixture()
    def client(self) -> resist.WebSocketClient:
        return resist.WebSocketClient("REVOLT_TOKEN")

    @pytest.mark.asyncio
    async def test_listener(self) -> None:
        fake = mock.AsyncMock()

        async def callback(arg: str) -> None:
            await fake(arg)

        def check() -> bool:
            return True

        listener = resist.Listener(once=False, callback=callback, check=check)

        assert listener.once is False
        assert listener.callback is callback
        assert listener.check is check

        await listener("foo")
        fake.assert_awaited_once_with("foo")

    @pytest.mark.asyncio
    async def test_collector(self) -> None:
        fake = mock.AsyncMock()

        async def callback(arg: list[int]) -> None:
            await fake(arg)

        def check() -> bool:
            return True

        collector = resist.Collector(
            timeout=timedelta(seconds=5),
            once=False,
            callback=callback,
            check=check,
            amount=5,
        )

        assert collector.once is False
        assert collector.callback is callback
        assert collector.check is check

        assert isinstance(collector.timeout, timedelta)
        assert collector.amount == 5
        assert collector.queue.maxsize == 5

        for i in range(5):
            await collector(i)

        fake.assert_awaited_once_with((0, 1, 2, 3, 4))
        fake.await_count = 0

        for i in range(5):
            await collector(i)
            await asyncio.sleep(1.5)

        fake.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_events(self, client: resist.WebSocketClient) -> None:
        client.loop = asyncio.get_running_loop()
        event = resist.Events.MESSAGE
        fake = mock.AsyncMock()

        assert event.name == "Message"
        assert isinstance(event.listeners, list)
        assert isinstance(event.collectors, list)
        assert hasattr(event, "subscribe")
        assert hasattr(event, "dispatch")

        async def callback(arg: str) -> None:
            await fake(arg)

        def check(arg: str) -> bool:
            return arg == "foo"

        listener = resist.Listener(once=False, callback=callback, check=check)
        event.subscribe(listener)

        tasks = event.dispatch(client, "foo")
        await asyncio.gather(*tasks)

        fake.assert_awaited_once_with("foo")
        fake.await_count = 0

        tasks = event.dispatch(client, "bar")
        await asyncio.gather(*tasks)

        fake.assert_not_awaited()

        for name, evt in resist.EVENT_MAPPING.items():
            assert isinstance(name, str)
            assert isinstance(evt, resist.Event)
            assert evt.name == name

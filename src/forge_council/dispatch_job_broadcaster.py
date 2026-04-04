"""In-process pub/sub for dispatch job snapshots (SSE / future WebSocket)."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any


class DispatchJobBroadcaster:
    """Fan-out job snapshots to subscribers on the same asyncio event loop."""

    def __init__(self) -> None:
        self._subs: dict[str, set[asyncio.Queue[dict[str, Any]]]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(
        self, job_id: str
    ) -> tuple[asyncio.Queue[dict[str, Any]], Callable[[], Awaitable[None]]]:
        q: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        async with self._lock:
            self._subs.setdefault(job_id, set()).add(q)

        async def unsub() -> None:
            async with self._lock:
                bucket = self._subs.get(job_id)
                if not bucket:
                    return
                bucket.discard(q)
                if not bucket:
                    del self._subs[job_id]

        return q, unsub

    async def publish(self, job_id: str, payload: dict[str, Any]) -> None:
        snap = dict(payload)
        async with self._lock:
            queues = list(self._subs.get(job_id, ()))
        for q in queues:
            q.put_nowait(snap)

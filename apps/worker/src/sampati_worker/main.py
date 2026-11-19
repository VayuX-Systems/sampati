# SPDX-License-Identifier: Apache-2.0
"""Sampati Worker main entry point."""

from __future__ import annotations

import asyncio
import logging
import signal
import sys

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sampati_api.config import get_settings
from sampati_api.logging import setup_logging
from sampati_api.database import init_db, close_db


logger = structlog.get_logger()


class Worker:
    """Background worker for scheduled jobs."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.scheduler = AsyncIOScheduler(timezone=self.settings.timezone)
        self._shutdown = asyncio.Event()

    async def start(self) -> None:
        """Start the worker."""
        setup_logging(self.settings.log_level)
        await init_db()

        # Register signal handlers
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self._shutdown.set)

        # TODO: Add scheduled jobs here
        # self.scheduler.add_job(self.run_collection_jobs, "interval", minutes=5)

        self.scheduler.start()
        logger.info("worker_started")

        # Wait for shutdown signal
        await self._shutdown.wait()
        await self.stop()

    async def stop(self) -> None:
        """Stop the worker."""
        logger.info("worker_stopping")
        self.scheduler.shutdown(wait=True)
        await close_db()
        logger.info("worker_stopped")

    async def run_collection_jobs(self) -> None:
        """Run plugin collection jobs."""
        # TODO: Implement collection job logic
        logger.debug("collection_job_tick")


async def main() -> None:
    worker = Worker()
    await worker.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
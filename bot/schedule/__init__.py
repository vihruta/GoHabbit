import asyncio
from typing import Optional
from datetime import datetime, timedelta
import aioschedule
from ..routers import prompt
from ..utils.services import Service


class ScheduleService(Service, aioschedule.Scheduler):
    def __init__(self, *, pending_jobs_interval: int = 60) -> None:
        aioschedule.Scheduler.__init__(self)
        self.pending_jobs_interval = pending_jobs_interval
        self.pending_jobs_task: Optional[asyncio.Task] = None
        self.is_running = False

    async def _run_pending_jobs(self):
        self.is_running = True
        while True:
            await asyncio.sleep(self.pending_jobs_interval)
            await self.run_pending()

    async def setup(self):
        self.pending_jobs_task = asyncio.create_task(self._run_pending_jobs())

    async def dispose(self):
        if self.pending_jobs_task and not self.pending_jobs_task.done():
            self.pending_jobs_task.cancel()

        self.pending_jobs_task = None
        self.is_running = False

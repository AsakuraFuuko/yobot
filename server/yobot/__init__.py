from typing import Optional, Union
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart

from .wrapper import BaseWrapper


class Yobot:
    def __init__(self,
                 bot_warpper: BaseWrapper,
                 quart_app: Quart,
                 ):
        self.bot = bot_warpper
        self.web = quart_app
        self.sched = AsyncIOScheduler()

    async def handle_msg(
        self,
        message: str,
        *,
        message_type: str,
        user_id: int,
        nickname: str,
        group_id: Optional[int] = None,
        group_role: Optional[str] = None,
    ):
        if message == 'ping':
            return self.bot.text('pong')

    def start_scheduler(self):
        self.sched.start()

# coding=utf-8
import asyncio

from aiocqhttp import CQHttp
from aiocqhttp.message import Message, MessageSegment, Event

from yobot import BaseWrapper, Yobot


class CoolqWrapper(BaseWrapper):

    mention_pattern = r'\[CQ:at,qq=(?P<mention>\d+)\]'

    group_role_dict = {
        'member': 2,
        'admin': 1,
        'owner': 0,
    }

    def __init__(self, cqbot):
        self.cqbot = cqbot

    def text(self, text):
        return MessageSegment.text(qq)

    def mention(self, qq):
        return MessageSegment.at(qq)

    def group_role(self, role):
        return self.group_role_dict[role]

    async def send_group_msg(self, group_id, message):
        await self.cqbot.send_group_msg(group_id=group_id, message=message)

    async def send_private_msg(self, user_id, message):
        await self.cqbot.send_private_msg(user_id=user_id, message=message)


cqbot = CQHttp(
    __name__,
    access_token=token,
    enable_http_post=False,
    server_app_kwargs={
        'static_url_path': 'assets',
        'static_folder': 'assets',
    },
)

coolq = CoolqWrapper(cqbot)

bot = Yobot(coolq, quartapp=cqbot.server_app)


@cqbot.on_message("group", "private")
async def _(e: Event):
    reply = await bot.handle_msg(
        message=e.raw_message,
        message_type=e.detail_type,
        user_id=e.user_id,
        nickname=e.sender.get('card') or e.sender['nickname'],
        group_id=e.group_id,
        group_role=e.sender.get('role'),
    )
    if reply is None:
        return None
    return {'reply': reply,
            'at_sender': False}


bot.start_scheduler()

cqbot.run(
    host='0.0.0.0',
    port=9444,
    debug=False,
    use_reloader=False,
    loop=asyncio.get_event_loop(),
)

# coding=utf-8
import asyncio

from mirai import (At, Friend, Group, Member, MessageChain, Mirai, Permission,
                   Plain)
from quart import Quart

from yobot import BaseWrapper, Yobot

qq = 123456  # 字段 qq 的值
authKey = 'abcdefg'  # 字段 authKey 的值
# httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.
mirai_api_http_locate = 'localhost:8080/'


class MiraiWrapper(BaseWrapper):

    mention_pattern = r'\[At::target=(?P<mention>\d+)\]'

    group_role_dict = {
        Permission.Owner: 0,
        Permission.Administrator: 1,
        Permission.Member: 2,
    }

    def __init__(self, miraiapp):
        self.miraiapp = miraiapp

    def text(self, text):
        return [Plain(text=text)]

    def mention(self, qq):
        return [At(target=qq)]

    def group_role(self, role):
        return self.group_role_dict[role]

    async def send_group_msg(self, group_id: int, message):
        await self.miraiapp.sendGroupMessage(group=group_id, message=message)

    async def send_private_msg(self, user_id: int, message):
        await self.miraiapp.sendFriendMessage(friend=user_id, message=message)


miraiapp = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")
mirai = MiraiWrapper(miraiapp)
quartapp = Quart(
    __name__,
    static_url_path='assets',
    static_folder='assets',
)
bot = Yobot(mirai, quartapp=quartapp)


@miraiapp.receiver("FriendMessage")
async def _(app: Mirai,
            message: MessageChain,
            friend: Friend,
            ):
    reply = await bot.handle_msg(
        message=message.toString(),
        message_type="private",
        user_id=friend.id,
        nickname=friend.nickname,
    )
    if reply is None:
        return
    await app.sendFriendMessage(friend, reply)


@miraiapp.receiver("GroupMessage")
async def _(app: Mirai,
            message: MessageChain,
            group: Group,
            member: Member,
            ):
    reply = await bot.handle_msg(
        message=message.toString(),
        message_type="group",
        user_id=member.id,
        nickname=member.memberName,
        group_id=group.id,
        group_role=member.permission,
    )
    if reply is None:
        return
    await app.sendGroupMessage(group, reply)

bot.start_scheduler()

if __name__ == "__main__":
    quartapp.run()
    miraiapp.run()

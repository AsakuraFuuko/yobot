# coding=utf-8
import asyncio

from quart import Quart, request, send_file

from yobot import BaseWrapper, Yobot


class DebuggerWrapper(BaseWrapper):

    mention_pattern = r'@(?P<mention>\d+)'

    def __init__(self):

    def text(self, text):
        return text

    def mention(self, qq):
        return f'@{qq}'

    def group_role(self, role):
        return role

    async def send_group_msg(self, group_id: int, message):
        print(f'send_group_msg[{group_id}]: {message}')

    async def send_private_msg(self, user_id: int, message):
        print(f'send_private_msg[{user_id}]: {message}')


debugger = DebuggerWrapper()
quartapp = Quart(
    __name__,
    static_url_path='assets',
    static_folder='assets',
)
bot = Yobot(debugger, quartapp=quartapp)


@quartapp.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'GET':
        return send_file('debugger.html')
    payload = await request.form
    reply = await bot.handle_msg(**payload)
    print(f'reply: {reply}')


bot.start_scheduler()

if __name__ == "__main__":
    quartapp.run()
    miraiapp.run()

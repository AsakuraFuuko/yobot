from abc import ABC, abstractclassmethod


class BaseWrapper(ABC):


class CoolqWrapper(BaseWrapper):
    mention_pattern: str

    @abstractclassmethod
    def text(self, text):
        ...

    @abstractclassmethod
    def mention(self, qq):
        ...

    @abstractclassmethod
    async def send_group_msg(self, group_id, message):
        ...

    @abstractclassmethod
    async def send_private_msg(self, user_id, message):
        ...

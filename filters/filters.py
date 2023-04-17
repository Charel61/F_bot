from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

class IsNameSurname(BaseFilter):
    async def __call__(self, message: Message) -> bool:

        name = message.text.split(' ')

        return len(name)<=3 and all(n.isalpha() for n in name)

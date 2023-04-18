from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from database.database import specialist_db, get_specialists

class IsNameSurname(BaseFilter):
    async def __call__(self, message: Message) -> bool:

        name = message.text.split(' ')

        return len(name)<=3 and all(n.isalpha() for n in name)



class IsSpecialist(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:


        return callback.data in get_specialists().keys()

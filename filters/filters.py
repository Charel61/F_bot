from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from database.database import specialist_db, get_specialists
from config_data.config import Config, load_config





class IsNameSurname(BaseFilter):
    async def __call__(self, message: Message) -> bool:

        name = message.text.split(' ')

        return len(name)<=3 and all(n.isalpha() for n in name)


#Фильтр проверяет есть ли  специалист в БД
class IsSpecialist(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data in get_specialists().keys():
            return callback.data
        else:
            return False


class IsNotAdmin(BaseFilter):
    def __init__(self, admin_id: int) -> None:

        self.admin_id = admin_id
    async def __call__(self, message: Message) -> bool:

        return message.from_user.id != self.admin_id

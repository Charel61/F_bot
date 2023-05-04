from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from database.database import specialist_db, get_specialists
from config_data.config import Config, load_config
from database.accessors import get_list_user_id, get_list_specialities, get_list_specialists, get_speciality_id





class IsNameSurname(BaseFilter):
    async def __call__(self, message: Message) -> bool:

        name = message.text.split(' ')

        return len(name)<=3 and all(n.isalpha() for n in name)


#Фильтр проверяет есть ли  специалист в БД
class IsSpecialist(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:

        list_specialists = await get_list_specialists()

        if callback.data in list_specialists:
            return callback.data
        else:
            return False


#Фильтр проверяет есть ли  специальность в БД MysQLlite
class IsSpeciality(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        list_specialities = await get_list_specialities()
        if callback.data in list_specialities:
            return callback.data
        else:
            return False






class IsNotAdmin(BaseFilter):
    def __init__(self, admin_id: int) -> None:

        self.admin_id = admin_id
    async def __call__(self, message: Message) -> bool:

        return message.from_user.id != self.admin_id


class KnownUser(BaseFilter):
     async def __call__(self, message: Message) -> bool:
        list_id = await get_list_user_id()
        print(list_id)
        print(message.from_user.id not in list_id)

        return message.from_user.id in list_id

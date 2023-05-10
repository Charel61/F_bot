
from lexicon.lexicon import LEXICON_RU
from database.accessors import get_user

user_db: dict[dict[str, str | int | bool]] = {}

async def show_user(id: int) -> dict|bool:
    user = await get_user(id)
    if id in user_db:
        return {
                'text':f'Имя: {user.name}\n'
                    f'Возраст: {user.age}\n'
                    f'Пол: {LEXICON_RU[user.gender]}\n'
                    f'Дата посещения: {user_db[id]["date_of_vizit"]}\n'
                    f'Время посещения: {user_db[id]["time_of_vizit"]}\n'
                    f'Специальность: {user_db[id]["speciality"]}\n'
                    f'Специалист: {user_db[id]["specialist"]}\n'
                    f'Получать новости: {user.wish_news}'
                    }

    else:
        return False

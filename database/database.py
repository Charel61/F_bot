
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_RU

user_db: dict[int, dict[str, str | int | bool]] = {}

def show_user(id: int) -> dict|bool:
    if id in user_db:
        return {
                'text':f'Имя: {user_db[id]["name"]}\n'
                    f'Возраст: {user_db[id]["age"]}\n'
                    f'Пол: {LEXICON_RU[user_db[id]["gender"]]}\n'
                    f'Дата посещения: {user_db[id]["date_of_vizit"]}\n'
                    f'Образование: {LEXICON_RU[user_db[id]["education"]]}\n'
                    f'Получать новости: {user_db[id]["wish_news"]}'}

    else:
        return False

from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_RU

user_dict: dict[int, dict[str, str | int | bool]] = {}

def show_user(id: int) -> dict|bool:
    if id in user_dict:
        return {
            'photo':user_dict[id]['photo_id'],
            'caption':f'Имя: {user_dict[id]["name"]}\n'
                    f'Возраст: {user_dict[id]["age"]}\n'
                    f'Пол: {LEXICON_RU[user_dict[id]["gender"]]}\n'
                    f'Образование: {LEXICON_RU[user_dict[id]["education"]]}\n'
                    f'Получать новости: {user_dict[id]["wish_news"]}'}

    else:
        return False

from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_RU

user_db: dict[dict[str, str | int | bool]] = {}

def show_user(id: int) -> dict|bool:
    if id in user_db:
        return {
                'text':f'Имя: {user_db[id]["name"]}\n'
                    f'Возраст: {user_db[id]["age"]}\n'
                    f'Пол: {LEXICON_RU[user_db[id]["gender"]]}\n'
                    f'Дата посещения: {user_db[id]["date_of_vizit"]}\n'
                    f'Время посещения: {user_db[id]["time_of_vizit"]}\n'
                    f'Образование: {LEXICON_RU[user_db[id]["education"]]}\n'
                    f'Получать новости: {user_db[id]["wish_news"]}'}

    else:
        return False



specialist_db: dict[dict[str, str | int | bool]] = {
    'speciality_1':{
        'specialist_1':
        {'experience':11,'education':LEXICON_RU['higher']},
        'specialist_2':
        {'experience':10,'education':LEXICON_RU['higher']},
        'specialist_3':
        {'experience':13,'education':LEXICON_RU['secondary']}

    },
     'speciality_2':{
        'specialist_4':
        {'experience':11,'education':LEXICON_RU['higher']},
        'specialist_5':
        {'experience':10,'education':LEXICON_RU['higher']},
        'specialist_6':
        {'experience':13,'education':LEXICON_RU['secondary']}

    },
     'speciality_3':{
        'specialist_9':
        {'experience':11,'education':LEXICON_RU['higher']},
        'specialist_8':
        {'experience':10,'education':LEXICON_RU['higher']},
        'specialist_10':
        {'experience':13,'education':LEXICON_RU['secondary']}

    }


}

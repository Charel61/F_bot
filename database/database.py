
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
def get_specialists():
    dict_specialist = {}
    for value in list(specialist_db.values()):
        dict_specialist |= value
    return dict_specialist

def show_specialist(specislist):
    dict_specialist = get_specialists()
    if specislist in dict_specialist:

        return  {'text':
        f'{specislist}\n\n\n'
        f'Опыт работы: {dict_specialist[specislist]["experience"]}\n'
        f'Образование: {dict_specialist[specislist]["education"]}'}

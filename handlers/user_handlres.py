
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from utils.utils import get_dates, get_time_list
from aiogram.types import (CallbackQuery, Message, PhotoSize)
from datetime import date

from aiogram import Router, F
from FSM.fsm import FSMFillForm
from database.database import show_user,user_db, specialist_db, show_specialist

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboard import create_inline_kb
from config_data.config import load_config, Config
from filters.filters import IsNameSurname, IsSpecialist, IsNotAdmin


config: Config = load_config('.env')
admin_id: int = int(config.admin_id)


router: Router = Router()

# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['/cancel'])


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/fillform'])
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени
@router.message(Command(commands='fillform'), StateFilter(default_state), IsNotAdmin(admin_id))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['name'])
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@router.message(StateFilter(FSMFillForm.fill_name), IsNameSurname())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text=f'{LEXICON_RU["age"]}, <b>{message.text}</b>!', parse_mode='HTML')
    await state.set_state(FSMFillForm.fill_age)



# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(text=LEXICON_RU['wrong_name'])

# Этот хэндлер будет срабатывать, если введен корректный возраст
# и переводить в состояние выбора датф
@router.message(StateFilter(FSMFillForm.fill_age),
            lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "age"
    await state.update_data(age=message.text)
    markup = create_inline_kb(3,*get_dates(date.today()))
    await message.answer(text=LEXICON_RU['date'],reply_markup=markup)
    # Устанавливаем состояние ожидания ввода даты
    await state.set_state(FSMFillForm.fill_date)


# Этот хэндлер будет срабатывать, если во время ввода возраста
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
    await message.answer(
        text=LEXICON_RU['wrong_age'])


# Этот хэндлер будет срабатывать, если введено корректная дата
# и переводить в состояние ожидания ввода времени
@router.callback_query(StateFilter(FSMFillForm.fill_date), Text(text=get_dates(date.today())))
async def process_choice_date(callback: CallbackQuery, state: FSMContext ):
    await state.update_data(date_of_vizit=callback.data)
    await callback.answer(f'Вы выбрали дату {callback.data}', show_alert=True)
    await callback.message.delete()
    # Создаем клваиатуру для выбора времени
    time_list = get_time_list()
    markup = create_inline_kb(len(time_list)//3,*time_list)

    await callback.message.answer(text=LEXICON_RU['time'],reply_markup=markup)

    # устанавливаем состояниие ожидания ввода времени
    await state.set_state(FSMFillForm.fill_time)




# Этот хэндлер будет срабатывать, если во время ввода даты
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_date))
async def warning_not_date(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])





#хэндлер, который будет срабатывать при верно выбранном времени и переключать
# в состояние ввода пола
@router.callback_query(StateFilter(FSMFillForm.fill_time), Text(text=get_time_list()))
async def process_choice_time(callback: CallbackQuery, state: FSMContext ):
    await state.update_data(time_of_vizit=callback.data)
    await callback.answer(f'Вы выбрали время {callback.data}', show_alert=True)
    await callback.message.delete()

    markup=create_inline_kb(2,'male','female')
    # Отправляем пользователю сообщение с клавиатурой
    await callback.message.answer(text=LEXICON_RU['gender'],
                         reply_markup=markup)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_gender)






# Этот хэндлер будет срабатывать, если во время ввода времени
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_time))
async def warning_not_time(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])

# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние выбора специальности
@router.callback_query(StateFilter(FSMFillForm.fill_gender),
                   Text(text=['male', 'female']))
@router.callback_query(StateFilter(FSMFillForm.fill_specialist),
                   Text(text='back'))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
    # по ключу "gender"
    if callback.data !='back':
        await state.update_data(gender=callback.data)
    # Удаляем сообщение с кнопками
    await callback.message.delete()


    # СОздаем клавиатуру для выбора специальности
    markup=create_inline_kb(2,*specialist_db.keys())
    await callback.message.answer(text=LEXICON_RU['choice_speciality'], reply_markup=markup)
    # Устанавливаем состояние ожидания выбора специальности
    await state.set_state(FSMFillForm.fill_speciality)


# Этот хэндлер будет срабатывать, если во время выбора пола
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_gender))
async def warning_not_gender(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])

# этот хэндлер будет срабатывать при выборе специальности и переводить
# пользователя в состояние выбора специалиста
@router.callback_query(StateFilter(FSMFillForm.fill_speciality),
                   Text(text=specialist_db.keys()))

async def process_choice_speciality(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
    # по ключу "speciality"

    await state.update_data(speciality=callback.data)

     # СОздаем клавиатуру для выбора специалиста
    markup=create_inline_kb(2,*specialist_db[callback.data].keys())
    await callback.message.edit_text(text=LEXICON_RU['choice_specialist'], reply_markup=markup)
    await state.set_state(FSMFillForm.fill_specialist)










#Этот хэндлер будет србатывать при выборе специалиста, показывать
# информацию о нём и предлагать выбрать его или вернуться к выбору специалистов.
@router.callback_query(StateFilter(FSMFillForm.fill_specialist),
                   IsSpecialist())
async def process_choise_specialist(callback: CallbackQuery, state: FSMContext):
    specialist = show_specialist(callback.data)
    await state.update_data(specialist = callback.data)
    markup = create_inline_kb(2,'confirm','back')
    await callback.message.edit_text(text=specialist['text'],reply_markup=markup)


# Этот хэндлер будет срабатывать, если во время ввыбора специальности или специалиста ввели что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_speciality))
@router.message(StateFilter(FSMFillForm.fill_specialist))
async def warning_not_time(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])





# Этот хэндлер будет срабатывать, если выбран специалист
# и переводить в состояние согласия получать новости
@router.callback_query(StateFilter(FSMFillForm.fill_specialist),
                   Text(text='confirm'))
async def process_education_press(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()

    # Создаем объект инлайн-клавиатуры
    markup = create_inline_kb(2,'yes','no')
    # Рудаляем сообщение с кнопками, отправляя
    # новый текст и новую клавиатуру

    await callback.message.answer(text=LEXICON_RU['news'],
                                     reply_markup=markup)
    # Устанавливаем состояние ожидания выбора получать новости или нет
    await state.set_state(FSMFillForm.fill_wish_news)



# Этот хэндлер будет срабатывать на выбор получать или
# не получать новости и выводить из машины состояний
@router.callback_query(StateFilter(FSMFillForm.fill_wish_news),
                   Text(text=['yes', 'no']))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о получении новостей по ключу "wish_news"
    await state.update_data(wish_news=callback.data == 'yes')
    await callback.message.delete()


    await state.set_state(FSMFillForm.fill_send_data)


    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_db[callback.from_user.id] = await state.get_data()

    markup = create_inline_kb(2,'send','do_not_send')

    user = show_user(callback.from_user.id)

    await callback.message.answer(

            text=user['text'],reply_markup=markup)

    # Этот хэндлер будет срабатывать, если во время согласия на получение
    # новостей будет введено/отправлено что-то некорректное
    @router.message(StateFilter(FSMFillForm.fill_wish_news))
    async def warning_not_wish_news(message: Message):
        await message.answer(text=LEXICON_RU['wrong'])


# Этот хэндлер будет срабатывать на выбор отправлять или не отправлять анкету
@router.callback_query(StateFilter(FSMFillForm.fill_send_data), Text(text=['send','do_not_send']))
async def process_send_data(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'send':

        await callback.message.forward(chat_id=admin_id)
        await callback.message.delete()

        # Отправляем в чат сообщение о сохранении двнных
        await callback.message.answer(text=LEXICON_RU['sent_data'])
    else:
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_RU['/fillform'])

    await state.clear()

# Этот хэндлер будет срабатывать, если во время согласия на отправку новостей будет введено, что-то некорректное
@router.callback_query(StateFilter(FSMFillForm.fill_send_data))
async def warning_not_send_data(message: Message):
        await message.answer(text=LEXICON_RU['wrong'])


# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@router.message(Command(commands='showdata'), StateFilter(default_state))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    user = show_user(message.from_user.id)
    if  user:
        await message.answer(

            text= user['text'])
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(text=LEXICON_RU['didnt_fill'])


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text=LEXICON_RU['dont_understand'])
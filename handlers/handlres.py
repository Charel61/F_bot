
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram.types import (CallbackQuery, Message, PhotoSize)

from aiogram import Router, F
from FSM.fsm import FSMFillForm
from database.database import user_dict, show_user

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboard import create_inline_kb
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
@router.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['name'])
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON_RU['age'])
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(text=LEXICON_RU['wrong_name'])




# Этот хэндлер будет срабатывать, если введен корректный возраст
# и переводить в состояние выбора пола
@router.message(StateFilter(FSMFillForm.fill_age),
            lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "age"
    await state.update_data(age=message.text)
    # Создаем объект инлайн-клавиатуры
    markup=create_inline_kb(2,'male','female','undefined_gender')
       # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text=LEXICON_RU['gender'],
                         reply_markup=markup)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_gender)


# Этот хэндлер будет срабатывать, если во время ввода возраста
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
    await message.answer(
        text=LEXICON_RU['wrong_age'])


# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние отправки фото
@router.callback_query(StateFilter(FSMFillForm.fill_gender),
                   Text(text=['male', 'female', 'undefined_gender']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
    # по ключу "gender"
    await state.update_data(gender=callback.data)
    # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_RU['photo'])
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMFillForm.upload_photo)


# Этот хэндлер будет срабатывать, если во время выбора пола
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_gender))
async def warning_not_gender(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])


# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора образования
@router.message(StateFilter(FSMFillForm.upload_photo),
            F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище
    # по ключам "photo_unique_id" и "photo_id"
    await state.update_data(photo_unique_id=largest_photo.file_unique_id,
                            photo_id=largest_photo.file_id)

    # Создаем объект инлайн-клавиатуры
    markup = create_inline_kb(2,'secondary','higher','no_edu')
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text=LEXICON_RU['edu'],
                         reply_markup=markup)
    # Устанавливаем состояние ожидания выбора образования
    await state.set_state(FSMFillForm.fill_education)


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMFillForm.upload_photo))
async def warning_not_photo(message: Message):
    await message.answer(text=LEXICON_RU['wrong_photo'])


# Этот хэндлер будет срабатывать, если выбрано образование
# и переводить в состояние согласия получать новости
@router.callback_query(StateFilter(FSMFillForm.fill_education),
                   Text(text=['secondary', 'higher', 'no_edu']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные об образовании по ключу "education"
    await state.update_data(education=callback.data)
    await callback.message.delete()

    # Создаем объект инлайн-клавиатуры
    markup = create_inline_kb(2,'yes','no')
    # Редактируем предыдущее сообщение с кнопками, отправляя
    # новый текст и новую клавиатуру

    await callback.message.answer(text=LEXICON_RU['news'],
                                     reply_markup=markup)
    # Устанавливаем состояние ожидания выбора получать новости или нет
    await state.set_state(FSMFillForm.fill_wish_news)


# Этот хэндлер будет срабатывать, если во время выбора образования
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_education))
async def warning_not_education(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])


# Этот хэндлер будет срабатывать на выбор получать или
# не получать новости и выводить из машины состояний
@router.callback_query(StateFilter(FSMFillForm.fill_wish_news),
                   Text(text=['yes', 'no']))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о получении новостей по ключу "wish_news"
    await state.update_data(wish_news=callback.data == 'yes')


    await state.set_state(FSMFillForm.F)


    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_dict[callback.from_user.id] = await state.get_data()



    # Завершаем машину состояний
    # await state.clear()
    # # Отправляем в чат сообщение о всохранении двнных
    # await callback.message.edit_text(text=LEXICON_RU['saved_data'])
    # Создаем объект инлайн-клавиатуры
    markup = create_inline_kb(2,'send','do_not_send')

    user = show_user(callback.from_user.id)

    await callback.message.answer_photo(
            photo=user['photo'],
            caption=user['caption'],reply_markup=markup)




# Этот хэндлер будет срабатывать, если во время согласия на получение
# новостей будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_wish_news))
async def warning_not_wish_news(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])


# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@router.message(Command(commands='showdata'), StateFilter(default_state))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    user = show_user(message.from_user.id)
    if  user:
        await message.answer_photo(
            photo = user['photo'],
            caption= user['caption'])
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(text=LEXICON_RU['didnt_fill'])


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, моя твоя не понимать')
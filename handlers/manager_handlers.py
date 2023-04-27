

from aiogram.filters import CommandStart, StateFilter, Command, Text
from aiogram.fsm.state import default_state
from FSM.fsm import FSMAddSpecialist, FSMManager, FSMAddSpeciality

from aiogram.types import  Message, CallbackQuery

from aiogram import Router
from aiogram.fsm.context import FSMContext
from filters.filters import IsNameSurname, IsSpeciality, IsNotAdmin

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboard import create_inline_kb
from database.accessors import get_list_specialities, get_speciality_id, get_speciality, add_specialist, add_speciality
from config_data.config import load_config, Config

router: Router = Router()
config: Config = load_config('.env')
admin_id: int = int(config.admin_id)
router.message.filter(~IsNotAdmin(admin_id))

# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать выполнить команды для управления базой данных
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/manage_db'])



# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/manage_db'])
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.message(Command(commands='manage_db'), StateFilter(default_state))
async def process_manage_db_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/start_manager'])
    await state.set_state(FSMManager.manage_db)



# Этот хэндлер будет срабатывать на команду /add_specialist в состоянии управления БД
# и предлагать добавить специалиста в базу данных
@router.message(Command(commands='add_specialist'),StateFilter(FSMManager.manage_db))
async def procces_add_specialist(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_specialist'])
    await state.set_state(FSMAddSpecialist.fill_name)




# Этот хэндлер будет срабатывать при правильно введенном имени и фамилии и предлагать выбрать
# специальность
@router.message(IsNameSurname(), StateFilter(FSMAddSpecialist.fill_name))
async def procces_add_specialist_name(message: Message, state: FSMContext):
    await state.update_data(name_specialist=message.text)
    list_specialities =await get_list_specialities()
    markup=create_inline_kb(1,*list_specialities )

    await message.answer(text=LEXICON_RU['choice_speciality'], reply_markup=markup)
    await state.set_state(FSMAddSpecialist.fill_speciality)

# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMAddSpecialist.fill_name))
async def warning_not_name(message: Message):
    await message.answer(text=LEXICON_RU['wrong_name'])




# Этот хэндлер будет срабатывать при правильно введенной специальности и предлагать
# ввести стаж работы
@router.callback_query(IsSpeciality(),StateFilter(FSMAddSpecialist.fill_speciality))
async def procces_add_specialist_speciality(callback: CallbackQuery, state: FSMContext):
    speciality_id = await get_speciality_id(callback.data)
    await state.update_data(speciality_id=speciality_id)
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_RU['expiriencne'])
    await state.set_state(FSMAddSpecialist.fill_expirience)

# Этот хэндлер будет срабатывать, если во время ввода cспециальности
# будет введено что-то некорректное
@router.message(StateFilter(FSMAddSpecialist.fill_speciality))
@router.message(StateFilter(FSMAddSpeciality.add_speciality))
async def warning_not_speciality(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])

# Этот хэндлер будет срабатывать при правильно введенном стаже и предлагать
# добавить специалиста в базу
@router.message(lambda x: x.text.isdigit() and 0 <= int(x.text) <= 70, StateFilter(FSMAddSpecialist.fill_expirience))
async def process_add_specialist_expirience(message: Message, state: FSMContext):
    await state.update_data(expirience=int(message.text))
    markup = create_inline_kb(2,'confirm','back')
    specialist = await state.get_data()
    speciality = await get_speciality(specialist['speciality_id'])


    await message.answer(text = f'{specialist["name_specialist"]}\n\n'
                                f'Специальность - {speciality}\n'
                                f'Стаж работы - {specialist["expirience"]}', reply_markup=markup)

    await state.set_state(FSMAddSpecialist.add_data)

# Этот хэндлер будет срабатывать, если во время ввода cтажа
# будет введено что-то некорректное
@router.message(StateFilter(FSMAddSpecialist.fill_expirience))
async def warning_not_exp(message: Message):
    await message.answer(text=LEXICON_RU['wrong_exp'])


# Этот хэндлер будет срабатывать при подтверждении или отмене ввода данных
@router.callback_query(Text(text=['confirm','back']), StateFilter(FSMAddSpecialist.add_data))
async def process_add_specialist_to_db(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'confirm':
        specialist = await state.get_data()
        await add_specialist(name=specialist['name_specialist'], experience=specialist['expirience'],speciality_id=specialist['speciality_id'])
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_RU['/manage_db'])
    await state.clear()




# Этот хэндлер будет срабатывать на команду /add_speciality в состоянии управления БД
# и предлагать добавить специалиста в базу данных
@router.message(Command(commands='add_speciality'),StateFilter(FSMManager.manage_db))
async def procces_add_specialist(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_speciality'])
    await state.set_state(FSMAddSpeciality.add_speciality)


# Этот хэндлер будет срабатывать при правильно введенной специальности и предлагать сохранить данные
@router.message(IsNameSurname(), StateFilter(FSMAddSpeciality.add_speciality))
async def procces_add_specialist_name(message: Message, state: FSMContext):
    await state.update_data(speciality=message.text)
    markup = create_inline_kb(2,'confirm','back')
    await message.reply(text=f'Добоавить в БД специальность {message.text}?',reply_markup=markup)
    await state.set_state(FSMAddSpeciality.add_data)







# Этот хэндлер будет срабатывать при подтверждении или отмене ввода данных
@router.callback_query(Text(text=['confirm','back']), StateFilter(FSMAddSpeciality.add_data))
async def process_add_specialist_to_db(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'confirm':
        specialist = await state.get_data()
        await add_speciality(specialist['speciality'])
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_RU['/manage_db'])
    await state.clear()







# Этот хэндлер будет срабатывать, если во время подтверждения
# будет введено что-то некорректное
@router.message(StateFilter(FSMAddSpecialist.add_data))
@router.message(StateFilter(FSMAddSpeciality.add_data))
async def warning_not_add(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])







# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text=LEXICON_RU['dont_understand'])
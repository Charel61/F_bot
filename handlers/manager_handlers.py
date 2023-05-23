

from aiogram.filters import CommandStart, StateFilter, Command, Text
from aiogram.fsm.state import default_state
from FSM.fsm import FSMAddSpecialist, FSMManager, FSMAddSpeciality

from aiogram.types import  Message, CallbackQuery

from aiogram import Router
from aiogram.fsm.context import FSMContext
from filters.filters import IsNameSurname, IsSpeciality, IsNotAdmin, IsSpecialist


from lexicon.lexicon import LEXICON_RU
from keyboards.keyboard import create_inline_kb
from database.accessors import (get_list_specialities, get_speciality_id, get_speciality, add_specialist, add_speciality, get_list_specialists, get_specialist,
                                del_specialist,del_speciality, get_specialist_by_id, edit_speciality)
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


# Этот хэндлер будет срабатывать при нажатии кнопки редактировать при просмотре данных о специалисте
@router.callback_query(Text(text='edit'),StateFilter(FSMManager.show_specialist))
async def procces_edit_specialist(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['/edit_specialist'])
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
# @router.message(StateFilter(FSMAddSpeciality.add_speciality))
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
@router.message(IsNameSurname(), StateFilter(FSMManager.edit_speciality))
async def procces_add_specialist_name(message: Message, state: FSMContext):
    await state.update_data(speciality=message.text)
    markup = create_inline_kb(2,'confirm','back')
    await message.reply(text=f'Подтвердите наименование специальности {message.text}?',reply_markup=markup)
    await state.set_state(FSMAddSpeciality.add_data)






# TODO: доделать процедуру, не добавляется мать ее# Этот хэндлер будет срабатывать при подтверждении или отмене ввода данных
@router.callback_query(Text(text=['confirm','back']), StateFilter(FSMAddSpeciality.add_data))
async def process_add_specialist_to_db(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'confirm':
        speciality = await state.get_data()
        speciality_id = await get_speciality_id(speciality['speciality'])
        print(speciality['speciality'],'_______________',speciality_id,'--------------------')
        try:
            await edit_speciality(await get_speciality_id(speciality['old_name_speciality']),speciality['speciality'])
        except KeyError:
            await add_speciality(speciality['speciality'])
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_RU['/manage_db'])
    await state.clear()


# Этот хэндлер будет срабатывать, если во время подтверждения
# будет введено что-то некорректное
@router.message(StateFilter(FSMAddSpecialist.add_data))
@router.message(StateFilter(FSMAddSpeciality.add_data))

async def warning_not_add(message: Message):
    await message.answer(text=LEXICON_RU['wrong'])


# Этот хэндлер будет срабатывать на комманду /show_specialist
@router.message(Command(commands='show_specialist'),StateFilter(FSMManager.manage_db))
async def procces_show_specialities(message: Message, state: FSMContext):
    list_specialities = await get_list_specialities()
    markup=create_inline_kb(1,*list_specialities, 'back' )

    await message.answer(text=LEXICON_RU['choice_speciality'], reply_markup=markup)
    await state.set_state(FSMManager.choice_specialities)


# Этот хэндлер будет срабатывать при правильно введенной специальности и предлагать
# выбрать специалиста
@router.callback_query(IsSpeciality(),StateFilter(FSMManager.choice_specialities))
async def procces_choice_specialist(callback: CallbackQuery, state: FSMContext):
    speciality_id = await get_speciality_id(callback.data)
    list_specialists = await get_list_specialists(speciality_id)
    markup = create_inline_kb(1, *list_specialists,'back')
    await callback.message.delete()
    await callback.message.answer(text = f'Для просмотра информации о специалисте нажмите нужную кнопку', reply_markup=markup)
    await state.set_state(FSMManager.choice_specialist)


# Этот хэндлер будет срабатывать при нажатии кнопки вернутсья и предлагать ввести команду
@router.callback_query(Text(text='back'),StateFilter(FSMManager.choice_specialities))
async def process_back_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['/start_manager'])
    await state.set_state(FSMManager.manage_db)

# этот хэндлер будет срабатывать если при выборе специальности будет отправлено что-то некорректное
@router.message(StateFilter(FSMManager.edit_speciality))
@router.message(StateFilter(FSMManager.choice_specialities))
async def process_back_press(message: Message):
    await message.answer(text=LEXICON_RU['wrong_but'])






# Этот хэндлер будет срабатывать при правильно выбраном специалисте и показывать информацию о нем
@router.callback_query( IsSpecialist(),StateFilter(FSMManager.choice_specialist))
async def process_show_specialist(callback: CallbackQuery, state: FSMContext):
    specialist = await get_specialist(name=callback.data)
    markup=create_inline_kb(2,'back','edit', 'delete')
    await state.update_data(specialist_id=specialist[3])
    await callback.message.answer(text=f'{specialist[0]}\n\n'
                                  f'Специальность: {specialist[1]}\n'
                                  f'Опыт работы по специальности: {specialist[2]} лет.', reply_markup=markup)
    await state.set_state(FSMManager.show_specialist)

# Этот хэндлер будет срабатывать при нажатии кнопки вернутсья и предлагать ввести специальность
@router.callback_query(Text(text='back'),StateFilter(FSMManager.choice_specialist))
async def process_back_press_2(callback:CallbackQuery, state: FSMContext):
    list_specialities = await get_list_specialities()
    markup=create_inline_kb(1,*list_specialities, 'back' )

    await callback.message.answer(text=LEXICON_RU['choice_speciality'], reply_markup=markup)
    await state.set_state(FSMManager.choice_specialities)
#
#
#  этот хэндлер будет срабатывать если при выборе специалиста будет отправлено что-то некорректное
@router.message(StateFilter(FSMManager.choice_specialist))
async def process_back_press_wrong(message: Message):
    await message.answer(text=LEXICON_RU['wrong_but'])


# Этот хэндлер будет срабатывать при нажатии кнопки вернутсья при просмотре данных о специалисте
@router.callback_query(Text(text='back'),StateFilter(FSMManager.show_specialist))
async def process_back_press_2(callback: CallbackQuery, state: FSMContext):
    list_specialities = await get_list_specialities()
    markup=create_inline_kb(1,*list_specialities, 'back' )

    await callback.message.answer(text=LEXICON_RU['choice_speciality'], reply_markup=markup)
    await state.clear()
    await state.set_state(FSMManager.choice_specialities)

# Этот хэндлер будет срабатывать при нажатии кнопки удалить при просмотре данных о специалисте
@router.callback_query(Text(text='delete'),StateFilter(FSMManager.show_specialist))
async def process_del_specialist(callback: CallbackQuery, state: FSMContext):
    data= await state.get_data()
    specialist_id = data['specialist_id']
    specialist = await get_specialist_by_id(specialist_id)

    markup = create_inline_kb(2,'confirm', 'back')
    await callback.message.answer(text=f'{LEXICON_RU["shure_del_spec"]} \n {specialist[0]} \n {specialist[1]}', reply_markup=markup)



# Этот хэндлер будет срабатывать при нажатии кнопки подтвердить при запросе удаления специалиста
@router.callback_query(Text(text='confirm'), StateFilter(FSMManager.show_specialist))
async def process_del_specialist_confirm(callback: CallbackQuery, state: FSMContext):
    data= await state.get_data()
    specialist_id = data['specialist_id']
    await del_specialist(specialist_id)
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(text=LEXICON_RU['/manage_db'])


# Этот хэндлер будет срабатывать если при просмотре специалиста будет введено что-нибудь неверное
@router.message(StateFilter(FSMManager.show_specialist))
async def process_wrong_show_specialist(message: Message):
    await message.answer(text=LEXICON_RU['wrong_but'])






@router.message(Command(commands='edit_speciality'),StateFilter(FSMManager.manage_db))
async def process_show_speciality(message: Message, state: FSMContext):
    list_specialities = await get_list_specialities()
    markup=create_inline_kb(1,*list_specialities, 'back' )
    await message.answer(text=LEXICON_RU['edit_speciality'],reply_markup=markup)
    await state.set_state(FSMManager.edit_speciality)

@router.callback_query(IsSpeciality(), StateFilter(FSMManager.edit_speciality))
async def process_choice_action_with_speciality(callback: CallbackQuery, state: FSMContext):

    await state.update_data(old_name_speciality=callback.data)
    markup = create_inline_kb(2, 'edit','delete', 'back')

    await callback.message.answer(text=f'{callback.data}\n\n{LEXICON_RU["choice_action"]}',reply_markup=markup)


@router.callback_query(Text(text=['edit','back']), StateFilter(FSMManager.edit_speciality))
async def process_edit_speciality(callback: CallbackQuery, state: FSMContext):
    if callback.data=='edit':
        await callback.message.answer(text=LEXICON_RU['/add_speciality'])
    else:
        await callback.message.answer(text=LEXICON_RU['/manage_db'])
        await state.clear()


@router.callback_query(Text(text=['delete']), StateFilter(FSMManager.edit_speciality))
async def process_delete_speciality(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup = create_inline_kb(2,'confirm','back')
    await callback.message.answer(text=f'{LEXICON_RU["shure_del_speciality"]} {data["old_name_speciality"]}?', reply_markup=markup)

@router.callback_query(Text(text=['confirm']), StateFilter(FSMManager.edit_speciality))
async def process_confitm_delete_speciality(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    speciality_id = await get_speciality_id(data['old_name_speciality'])
    await del_speciality(speciality_id)
    await state.clear()
    await callback.message.answer(text=LEXICON_RU['/manage_db'])





















# TODO: написать процедуру просмотра заказов.



@router.message(StateFilter(FSMManager.manage_db))
async def send_echo(message: Message):
    await message.answer(text=LEXICON_RU['/start_manager'])

# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text=LEXICON_RU['dont_understand'])
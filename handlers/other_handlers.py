

from aiogram.filters import CommandStart, StateFilter, Command, Text
from aiogram.fsm.state import default_state

from aiogram.types import  Message, CallbackQuery

from aiogram import Router
from aiogram.fsm.context import FSMContext
from filters.filters import IsNameSurname

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboard import create_inline_kb
from database.accessors import get_list_specialities, get_speciality_id, get_list_specialities_not_cor

router: Router = Router()

# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands='add_specialist'),StateFilter(default_state))
async def procces_add_specialist(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_specialist'])


@router.message(IsNameSurname(), StateFilter(default_state))
async def procces_add_specialist_name(message: Message, state: FSMContext):
    await state.update_data(name_specialist=message.text)
    list_specialities =await get_list_specialities()
    markup=create_inline_kb(3,*list_specialities )

    await message.answer(text=LEXICON_RU['choice_speciality'], reply_markup=markup)


@router.callback_query(Text(text=get_list_specialities_not_cor()),StateFilter(default_state))
async def procces_add_specialist_speciality(callback: CallbackQuery, state: FSMContext):
    speciality_id = await get_speciality_id(callback.data)
    await state.update_data(specility_id=speciality_id)













# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text=LEXICON_RU['dont_understand'])
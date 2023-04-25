

from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state

from aiogram.types import  Message

from aiogram import Router

from lexicon.lexicon import LEXICON_RU

router: Router = Router()

# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router



# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text=LEXICON_RU['dont_understand'])
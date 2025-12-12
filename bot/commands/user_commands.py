from aiogram import Router, types
from aiogram.filters import Command

from bot.keyboards import unsubscribe_kb

router = Router()


@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: types.Message):
    await message.answer("Вы хотите отменить Premium подписку?",
                         reply_markup=unsubscribe_kb.first_unsubscribe_stage_keyboard)



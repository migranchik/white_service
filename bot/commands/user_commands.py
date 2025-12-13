from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from bot.keyboards import unsubscribe_kb

router = Router()


@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: types.Message):
    await message.answer("Вы хотите отменить Premium подписку?",
                         reply_markup=unsubscribe_kb.first_unsubscribe_stage_keyboard)


@router.message(Command("policy"))
async def cmd_policy(message: types.Message):
    await message.answer('<b><a href="https://telegra.ph/Politika-konfidencialnosti-12-13-13">Политика конфиденциальности</a></b>',
                         parse_mode=ParseMode.HTML)


@router.message(Command("agreement"))
async def cmd_agreement(message: types.Message):
    await message.answer('<b><a href="https://telegra.ph/Polzovatelskoe-soglashenie-12-13-9">Пользовательское соглашение</a></b>',
                         parse_mode=ParseMode.HTML)


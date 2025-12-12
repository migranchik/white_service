from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..keyboards import support_kb

router = Router()


@router.callback_query(F.data.startswith('support'))
async def support_menu(callback: CallbackQuery):
    await callback.message.edit_text("❓ <b>Помощь</b> \n\n"
                                     "👻 <b>Поддержка</b>: @WhiteVpnSupport",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=support_kb.support_keyboard)

    await callback.answer()


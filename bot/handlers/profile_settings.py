from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..keyboards import profile_settings_kb

router = Router()


@router.callback_query(F.data.startswith("settings"))
async def profile_settings(callback: CallbackQuery):
        await callback.message.edit_text("⚙️ <b>Настройки</b> \n\n"
                                         "Автоплатеж: <b>включен</b>\n\n"
                                         "Вы можете отменить подписку в любой момент. Таким образом автоплатеж отменится. Для этого, отправьте команду /unsubscribe.",
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=profile_settings_kb.profile_settings_keyboard)

        await callback.answer()

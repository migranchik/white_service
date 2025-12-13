from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..keyboards import profile_menu_kb

from core.services import ProfileService
from core.services import UsersService
from infra.db.connection import async_session_maker
from infra.db.models import SubscriptionStatus

router = Router()


@router.callback_query(F.data.startswith("profile"))
async def profile_menu(callback: CallbackQuery):
    async with async_session_maker() as session:
        profile_service = ProfileService(session)
        profile_stats = await profile_service.get_profile(callback.from_user.id)

    subscription_status_text = "У вас подключена подписка WhiteVPN Premium🐝" if profile_stats['subscription_status'] == SubscriptionStatus.ACTIVE else "Ваша подписка WhiteVPN Premium истекла💔"

    await callback.message.edit_text(f"{subscription_status_text}\n\n"
                                     f"Подписка активна до: {profile_stats['subscription_expire'].strftime('%d.%m.%Y')} \n"
                                     f"Ниже ваш постоянный ключ - ключ к свободе\n\n"
                                     f"{profile_stats['subscription_link']}\n\n"
                                     f"<i>Ваш ID: {profile_stats['tg_id']}</i> \n"
                                     f"<i>Количество приглашенных: {profile_stats['referrals_count']}</i>\n"
                                     f"<i>Баланс: {profile_stats['balance']} руб.</i>\n"
                                     f"<i>Заработано за все время: {profile_stats['referrals_income']} руб.</i>",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=profile_menu_kb.profile_menu_keyboard,
                                     disable_web_page_preview=True)

    await callback.answer()


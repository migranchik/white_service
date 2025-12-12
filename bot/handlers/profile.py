from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..keyboards import profile_menu_kb

from core.services.users_service import UsersService
from infra.db.connection import async_session_maker
from infra.db.models import SubscriptionStatus

router = Router()


@router.callback_query(F.data.startswith("profile"))
async def profile_menu(callback: CallbackQuery):
    async with async_session_maker() as session:
        service = UsersService(session)
        user = await service.get_user_by_tg_id(callback.from_user.id)
        subscription = user.subscription
        vpn_account = user.vpn_account
        referral_stats = await service.get_referral_stats(callback.from_user.id)
    print(subscription.status, SubscriptionStatus.ACTIVE)
    subscription_status_text = "У вас подключена подписка WhiteVPN Premium🐝" if subscription.status == SubscriptionStatus.ACTIVE else "Ваша подписка WhiteVPN Premium истекла💔"
    await callback.message.edit_text(f"{subscription_status_text}\n\n"
                                     f"Подписка активна до: {subscription.expires_at.strftime("%d.%m.%Y")} \n"
                                     f"Ниже ваш постоянный ключ - ключ к свободе\n\n"
                                     f"{vpn_account.subscription_link}\n\n"
                                     f"<i>Ваш ID: {referral_stats.user.tg_id}</i> \n"
                                     f"<i>Количество приглашенных: {referral_stats.total_referrals}</i>\n"
                                     f"<i>Баланс: {referral_stats.balance} руб.</i>\n"
                                     f"<i>Заработано за все время: {referral_stats.total_earned} руб.</i>",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=profile_menu_kb.profile_menu_keyboard,
                                     disable_web_page_preview=True)

    await callback.answer()


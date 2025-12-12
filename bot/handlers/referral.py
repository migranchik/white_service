from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..keyboards import referral_menu_kb
from ..utils.ref_link_creator import RefLinkCreator
from ..utils.reffer_qr_generator import generate_qr_image

from configs.settings import settings

from core.services.users_service import UsersService
from infra.db.connection import async_session_maker

router = Router()


@router.callback_query(F.data.startswith('referral'))
async def support_menu(callback: CallbackQuery):
    async with async_session_maker() as session:
        service = UsersService(session)
        ref_code = await service.get_ref_code(callback.from_user.id)
        ref_link = RefLinkCreator.create(ref_code)
        referral_stats = await service.get_referral_stats(callback.from_user.id)

    await callback.answer("🔄Генерируем QR-код...")

    qr = await generate_qr_image(ref_link)
    await callback.message.edit_media(
        types.InputMediaPhoto(
            media=qr,
            caption=f"<b>Приглашайте людей и зарабатывайте вместе с нами💰</b> \n\n"
                    f"Приглашенный человек получит 7 дней Premium подписки \n"
                    f"А вы — <b>{int(settings.REFERRAL_PERCENT * 100)}% с его покупок</b> \n\n"
                    f"—  Приглашено пользователей: {referral_stats.total_referrals}* \n\n"
                    f"🔗 <b>Ваша ссылка для приглашения:</b> \n"
                    f"{ref_link} \n\n"
                    f"📱 <i>QR-код выше содержит вашу реферальную ссылку - перейдя по ней можно  получить 7 дней premium бесплатно!</i> \n\n"
                    f"<i>* более подробная статистика о доходе в вашем профиле</i>",
            parse_mode=ParseMode.HTML,
        ),
        reply_markup=referral_menu_kb.get_referral_menu(ref_link)
    )


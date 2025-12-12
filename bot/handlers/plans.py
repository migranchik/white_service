from typing import List

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..keyboards import plans_kb

from core.services.plans_service import PlansService
from infra.db.connection import async_session_maker


router = Router()

plans_temp = []

@router.callback_query(F.data.startswith("plans"))
async def profile_menu(callback: CallbackQuery):
    async with async_session_maker() as session:
        plans_service = PlansService(session)
        plans_list = await plans_service.get_all_active_plans()


    await callback.message.answer_photo(photo="https://i.ibb.co/3QWwCv2/plans-image.png",
                                        caption="<b>Тарифные планы</b> \n\n"
                                     "Что получает <b>Premium</b> пользователь? \n"
                                     "— Обход глушилок мобильной сети \n"
                                     "— Просмотр Youtube без рекламы \n"
                                     "— Неограниченный трафик \n"
                                     "— Круглосуточная тех. поддержка \n\n"
                                     "Выберите наиболее подходящий вам тариф и познайте качество нашего сервиса! С нами уже более 1.000 довольных пользователей",
                                        parse_mode=ParseMode.HTML,
                                        reply_markup=plans_kb.get_plans_kb(plans_list ))

    await callback.answer()


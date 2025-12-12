from aiogram import Router, types, F
from aiogram.types import CallbackQuery

from bot.keyboards import unsubscribe_kb


router = Router()

@router.callback_query(F.data.startswith("no_unsubscribe"))
async def no_unsubscribe(callback: CallbackQuery):
    await callback.message.edit_text("🧡Cупер, мы рады, что вы остаетесь с нами!")
    await callback.answer()

@router.callback_query(F.data.startswith("second_stage_unsubscribe"))
async def no_unsubscribe(callback: CallbackQuery):
    await callback.message.edit_text("После отмены подписки Premium, вы потеряете Youtube без рекламы, безлимитный трафик и обход беспилотной опасности \n\n"
                                     "Сохраним данные преимущества?",
                                     reply_markup=unsubscribe_kb.second_unsubscribe_stage_keyboard
                                     )
    await callback.answer()


@router.callback_query(F.data.startswith("final_unsubscribe"))
async def no_unsubscribe(callback: CallbackQuery):
    await callback.message.edit_text("Нам жаль, что мы подвели вас! Подписка отменена, функции Premium подписки будут работать до конца оплаченного периода.")
    await callback.answer()

    # TODO добавить отключение автоплатежа

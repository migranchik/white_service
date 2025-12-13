import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states.admin import AdminBroadcast
from bot.keyboards.admin.broadcast import (
    admin_menu_kb,
    broadcast_segments_kb,
    broadcast_confirm_kb,
)

from infra.db.connection import async_session_maker
from infra.repositories.users_repo import UsersRepository  # твой путь

admin_broadcast_router = Router()

# Тут будем складывать выбранное, чтобы не плодить отдельные таблицы
# state["broadcast_text"], state["broadcast_segment"]


@admin_broadcast_router.message(F.text == "/admin")
async def admin_start(message: Message):
    await message.answer("Админ-меню:", reply_markup=admin_menu_kb())


@admin_broadcast_router.callback_query(F.data == "admin:menu")
async def admin_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Админ-меню:", reply_markup=admin_menu_kb())
    await call.answer()


@admin_broadcast_router.callback_query(F.data == "admin:broadcast")
async def broadcast_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminBroadcast.waiting_text)
    await call.message.edit_text(
        "📣 Рассылка\n\nОтправь текст рассылки одним сообщением.\n"
        "Можно с переносами строк.\n\n"
        "Отмена: /cancel"
    )
    await call.answer()


@admin_broadcast_router.message(AdminBroadcast.waiting_text)
async def broadcast_got_text(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    if not text:
        await message.answer("Текст пустой. Отправь нормальный текст 🙂")
        return

    await state.update_data(broadcast_text=text)
    await state.set_state(AdminBroadcast.waiting_segment)
    await message.answer(
        "Кому отправляем?",
        reply_markup=broadcast_segments_kb()
    )


@admin_broadcast_router.callback_query(AdminBroadcast.waiting_segment, F.data.startswith("broadcast:segment:"))
async def broadcast_pick_segment(call: CallbackQuery, state: FSMContext):
    segment = call.data.split(":")[-1]  # all/active/inactive
    await state.update_data(broadcast_segment=segment)
    data = await state.get_data()
    text = data.get("broadcast_text", "")

    seg_name = {"all": "Всем", "active": "Только с подпиской", "inactive": "Без подписки"}.get(segment, segment)

    await state.set_state(AdminBroadcast.waiting_confirm)
    await call.message.edit_text(
        f"✅ Превью рассылки\n\n"
        f"Сегмент: *{seg_name}*\n\n"
        f"{text}",
        reply_markup=broadcast_confirm_kb(),
        parse_mode="Markdown"
    )
    await call.answer()


@admin_broadcast_router.callback_query(AdminBroadcast.waiting_confirm, F.data == "broadcast:edit")
async def broadcast_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminBroadcast.waiting_text)
    await call.message.edit_text("Ок, отправь новый текст рассылки.\n\nОтмена: /cancel")
    await call.answer()


@admin_broadcast_router.callback_query(AdminBroadcast.waiting_confirm, F.data == "broadcast:cancel")
async def broadcast_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Отменил ✅", reply_markup=admin_menu_kb())
    await call.answer()


@admin_broadcast_router.message(F.text == "/cancel")
async def cancel_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено ✅", reply_markup=admin_menu_kb())


@admin_broadcast_router.callback_query(AdminBroadcast.waiting_confirm, F.data == "broadcast:send")
async def broadcast_send(call: CallbackQuery, state: FSMContext, bot):
    data = await state.get_data()
    text = data.get("broadcast_text")
    segment = data.get("broadcast_segment", "all")

    if not text:
        await call.answer("Нет текста рассылки", show_alert=True)
        return

    async with async_session_maker() as session:
        users_repo = UsersRepository(session)

        if segment == "active":
            tg_ids = await users_repo.get_tg_ids_active()
        elif segment == "inactive":
            tg_ids = await users_repo.get_tg_ids_inactive()
        else:
            tg_ids = await users_repo.get_tg_ids_all()

    total = len(tg_ids)
    await call.message.edit_text(f"🚀 Начинаю рассылку… получателей: {total}")
    await call.answer()

    sent, failed = 0, 0

    # анти-флуд: 25-28 msg/sec лучше не превышать. Сделаем 20/сек.
    for tg_id in tg_ids:
        try:
            await bot.send_message(chat_id=tg_id, text=text)
            sent += 1
        except Exception:
            failed += 1

        if (sent + failed) % 20 == 0:
            await asyncio.sleep(1)

    await state.clear()
    await call.message.answer(
        f"✅ Готово.\n\nОтправлено: {sent}\nОшибок: {failed}",
        reply_markup=admin_menu_kb()
    )

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📣 Рассылка", callback_data="admin:broadcast")
    return kb.as_markup()

def broadcast_segments_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="👥 Всем", callback_data="broadcast:segment:all")
    kb.button(text="✅ Только с подпиской", callback_data="broadcast:segment:active")
    kb.button(text="❌ Без подписки", callback_data="broadcast:segment:inactive")
    kb.button(text="⬅️ Назад", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()

def broadcast_confirm_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Отправить", callback_data="broadcast:send")
    kb.button(text="✏️ Изменить текст", callback_data="broadcast:edit")
    kb.button(text="❌ Отмена", callback_data="broadcast:cancel")
    kb.adjust(1)
    return kb.as_markup()

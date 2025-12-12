from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

first_unsubscribe_stage = [
    [InlineKeyboardButton(text="Нет, погорячился 🤩", callback_data="no_unsubscribe")],
    [InlineKeyboardButton(text="Да", callback_data="second_stage_unsubscribe")],
]

first_unsubscribe_stage_keyboard = InlineKeyboardMarkup(inline_keyboard=first_unsubscribe_stage)

second_unsubscribe_stage = [
    [InlineKeyboardButton(text="Давайте сохраним💪", callback_data="no_unsubscribe")],
    [InlineKeyboardButton(text="Нет, отключить", callback_data="final_unsubscribe")],
]

second_unsubscribe_stage_keyboard = InlineKeyboardMarkup(inline_keyboard=second_unsubscribe_stage)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton(text="Пригласить и заработать", callback_data="referral")],
    [InlineKeyboardButton(text="← Назад", callback_data="profile")]
]

profile_settings_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

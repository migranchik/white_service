from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton(text="❓Написать в поддержку", url="https://t.me/WhiteVpnSupport")],
    [InlineKeyboardButton(text="🗞 Новости сервиса", url="https://t.me/WhiteVpnChannel")],
    [InlineKeyboardButton(text="← Назад", callback_data="back_to_main_menu")],
]

support_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

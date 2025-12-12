from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton(text="Помощь", callback_data="support"), InlineKeyboardButton(text="Профиль", callback_data="profile")],
    [InlineKeyboardButton(text="⚡️Установить VPN⚡️", callback_data="install_vpn")],
    [InlineKeyboardButton(text="Тарифы", callback_data="plans")],
    [InlineKeyboardButton(text="Пригласить и заработать", callback_data="referral")],
]

main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings"), InlineKeyboardButton(text="⚡️Установить VPN⚡️", callback_data="install_vpn")],
    [InlineKeyboardButton(text="Пригласить и заработать", callback_data="referral")],
    [InlineKeyboardButton(text="← Назад", callback_data="back_to_main_menu")]
]

profile_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

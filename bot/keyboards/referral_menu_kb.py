from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_referral_menu(referral_link: str):
    keyboard = [
        [InlineKeyboardButton(text="Пригласить",
                              url=f"https://t.me/share/url?url={referral_link}&text=Попробуй установить WhiteVPN, "
                                  f"глушилки интернета обходит, быстро и надежно работает, "
                                  f"короче кайф")],
        [InlineKeyboardButton(text="⚡️Установить VPN⚡️", callback_data="install_vpn")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_main_menu")],
    ]

    referral_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return referral_menu_keyboard
from urllib.parse import quote
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_referral_menu(referral_link: str):
    share_url = (
        "https://t.me/share/url"
        f"?url={quote(referral_link, safe='')}"
        f"&text={quote('Попробуй установить WhiteVPN, глушилки интернета обходит, быстро и надежно работает, короче кайф', safe='')}"
    )

    keyboard = [
        [InlineKeyboardButton(text="Пригласить", url=share_url)],
        [InlineKeyboardButton(text="⚡️Установить VPN⚡️", callback_data="install_vpn")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

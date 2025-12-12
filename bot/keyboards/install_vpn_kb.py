from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from configs.settings import settings

def get_install_vpn_keyboard(devices: dict):
    keyboard = []
    items = list(devices.items())

    for i in range(0, len(items), 2):
        if i + 1 < len(items):
            pair = items[i:i + 2]
            keyboard.append([InlineKeyboardButton(text=pair[0][1]["name"], callback_data=f"manual_{pair[0][0]}"), InlineKeyboardButton(text=pair[1][1]["name"], callback_data=f"manual_{pair[1][0]}")])
        else:
            keyboard.append([InlineKeyboardButton(text=items[i][1]["name"], callback_data=f"manual_{items[i][0]}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_manual_keyboard(url_schema: str, subscription_link: str) -> InlineKeyboardMarkup:
    connection_url = f"{settings.API_LINK}api/v1/redirect_dl?url={url_schema}{subscription_link}"
    keyboard = [
        [InlineKeyboardButton(text="Подключиться в 1 клик", url=connection_url)],
        [InlineKeyboardButton(text="Не смог подключить", callback_data=f"support")],
        [InlineKeyboardButton(text="Другие устройства", callback_data="another_device")]

    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
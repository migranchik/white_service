from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

def get_manual_keyboard(devices: dict, device_id):
    keyboard = [
        [InlineKeyboardButton(text="Подключиться в 1 клик", url=f"https://google.com")],
        [InlineKeyboardButton(text="Не смог подключить", callback_data=f"support")],
        [InlineKeyboardButton(text="Другие устройства", callback_data="another_device")]

    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
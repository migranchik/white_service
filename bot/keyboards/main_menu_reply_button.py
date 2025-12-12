from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_reply_button = ReplyKeyboardMarkup(resize_keyboard=True,
                                                keyboard=[
                                                    [KeyboardButton(text="Главное меню")]
                                                ])
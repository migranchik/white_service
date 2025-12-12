from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from infra.db.models import PlanBase


def get_payment_button(confirmation_url: str) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text="Оплатить подписку😇", url=confirmation_url)]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

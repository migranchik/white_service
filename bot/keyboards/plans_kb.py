from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from infra.db.models import PlanBase


def get_plans_kb(plans_info: list[PlanBase]) -> InlineKeyboardMarkup:
    keyboard = list()
    for plan in plans_info:
        keyboard.append([InlineKeyboardButton(text=plan.name, callback_data=f"choose_plan_{plan.id}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

class AdminOnly(BaseFilter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = set(admin_ids)

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = event.from_user
        return bool(user and user.id in self.admin_ids)
